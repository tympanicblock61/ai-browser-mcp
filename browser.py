# browser.navigate: [url] — navigates to the specified URL
# browser.reload: [] — reloads the current page
# browser.go_back: [] — goes to the previous page in history
# browser.go_forward: [] — goes to the next page in history
# browser.click: [selector] — clicks on the first matching element
# browser.double_click: [selector] — double-clicks the element
# browser.right_click: [selector] — right-clicks the element
# browser.input_text: [selector, text] — types text into an input field
# browser.clear_input: [selector] — clears the input field
# browser.submit: [selector] — submits a form/button
# browser.hover: [selector] — hovers over an element
# browser.scroll_to: [selector] — scrolls to the element
# browser.scroll_by: [x, y] — scrolls by a pixel amount
# browser.press_key: [key] — simulates a keyboard key press
# browser.element_exists: [selector] — returns whether the selector matches any element
# browser.get_text: [selector] — returns inner text of the element
# browser.get_all_text: [] — returns all visible text on the page
# browser.get_html: [] — returns the full page HTML
# browser.get_outer_html: [selector] — returns outer HTML of an element
# browser.get_attr: [selector, attribute] — returns a specific attribute (e.g., href, src)
# browser.get_value: [selector] — returns value of an input field
# browser.get_tag: [selector] — returns the tag name of the element
# browser.list_links: [] — returns all <a> tags as {text, href}
# browser.list_buttons: [] — returns all <button> or clickable elements
# browser.list_inputs: [] — returns all <input> and <textarea> elements
# browser.list_elements: [selector] — returns matching elements and basic info
# browser.select_option: [selector, value] — selects <option> by value
# browser.check: [selector] — checks a checkbox
# browser.uncheck: [selector] — unchecks a checkbox
# browser.toggle: [selector] — toggles checkbox/radio/switch
# browser.set_checkbox: [selector, state] — sets checkbox to True/False
# browser.wait_for: [selector, timeout] — waits for selector to exist or timeout
# browser.wait_until_text: [selector, text, timeout] — waits for element to contain text
# browser.sleep: [seconds] — pauses execution for N seconds
# browser.screenshot: [] — takes a full-page screenshot (base64 or path)
# browser.element_screenshot: [selector] — screenshots a specific element

# network.list_requests: [] — returns a list of all captured network requests
# network.get_request: [request_id] — returns full info for a specific request
# network.get_request_body: [request_id] — returns the body of a specific request (if captured)
# network.get_response: [request_id] — returns response headers, status, body, etc.
# network.get_response_body: [request_id] — returns the raw body of a specific response
# network.get_all_headers: [request_id] — returns all request and response headers
# network.search_requests: [url_pattern] — returns requests matching a URL substring or regex
# network.filter_by_method: [method] — returns requests using the specified HTTP method (e.g. GET, POST)
# network.filter_by_status: [status_code] — returns responses with the given HTTP status
# network.find_json_responses: [] — returns all responses with \`Content-Type: application/json\`
# network.find_errors: [] — returns all failed requests (4xx/5xx)
# network.find_redirects: [] — returns all 3xx response requests
# network.get_query_params: [request_id] — extracts query parameters from a URL
# network.get_post_data: [request_id] — returns POST form or JSON body (if captured)
# network.get_json_body: [request_id] — parses request or response as JSON
# network.find_requests_to_domain: [domain] — returns all requests sent to a specific domain
# network.find_requests_containing: [text] — returns requests/responses containing specific string in body
# network.get_timing: [request_id] — returns timing info (start time, duration, etc.)
# network.get_size: [request_id] — returns request and response size (headers + body)
# network.get_mime_type: [request_id] — returns the MIME type of the response
# network.get_cookies: [request_id] — extracts `Set-Cookie` or sent cookies from headers

import inspect
import re
from enum import Enum
from typing import get_origin, get_args, Union, List, Dict

import docstring_parser
from fastmcp import FastMCP
from selenium import webdriver
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as SeleniumKeys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.bidi.network import Request

def toolcall(func):
    """Decorator to mark methods as tool calls."""
    func._is_toolcall = True
    return func

class NetworkHandler:
    # noinspection PyTypeChecker
    def __init__(self):
        self._driver: WebDriver = None
        self.requests = set()

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value: WebDriver):
        self._driver = value
        # this is causing errors, fix in later versions
        self._driver.network.add_request_handler('before_request', self.before_request, None, None)


    def before_request(self, req: Request):
        self.requests.add(req)

    @toolcall
    def list_requests(self) -> set[Request]:
        return self.requests.copy()


# could execute js instead that sends a key press event
# use mozilla docs for the key ids etc
class Keys(Enum):
    NULL = SeleniumKeys.NULL
    CANCEL = SeleniumKeys.CANCEL
    HELP = SeleniumKeys.HELP
    BACKSPACE = SeleniumKeys.BACKSPACE
    BACK_SPACE = BACKSPACE
    TAB = SeleniumKeys.TAB
    CLEAR = SeleniumKeys.CLEAR
    RETURN = SeleniumKeys.RETURN
    ENTER = SeleniumKeys.ENTER
    SHIFT = SeleniumKeys.SHIFT
    LEFT_SHIFT = SHIFT
    RIGHT_SHIFT = SeleniumKeys.RIGHT_SHIFT
    CONTROL = SeleniumKeys.CONTROL
    LEFT_CONTROL = CONTROL
    RIGHT_CONTROL = SeleniumKeys.RIGHT_CONTROL
    ALT = SeleniumKeys.ALT
    LEFT_ALT = ALT
    RIGHT_ALT = SeleniumKeys.RIGHT_ALT
    PAUSE = SeleniumKeys.PAUSE
    ESCAPE = SeleniumKeys.ESCAPE
    SPACE = SeleniumKeys.SPACE
    PAGE_UP = SeleniumKeys.PAGE_UP
    PAGE_DOWN = SeleniumKeys.PAGE_DOWN
    END = SeleniumKeys.END
    HOME = SeleniumKeys.HOME
    LEFT = SeleniumKeys.LEFT
    ARROW_LEFT = LEFT
    UP = SeleniumKeys.UP
    ARROW_UP = UP
    RIGHT = SeleniumKeys.RIGHT
    ARROW_RIGHT = RIGHT
    DOWN = SeleniumKeys.DOWN
    ARROW_DOWN = DOWN
    INSERT = SeleniumKeys.INSERT
    DELETE = SeleniumKeys.DELETE
    SEMICOLON = SeleniumKeys.SEMICOLON
    EQUALS = SeleniumKeys.EQUALS

    NUMPAD0 = SeleniumKeys.NUMPAD0
    NUMPAD1 = SeleniumKeys.NUMPAD1
    NUMPAD2 = SeleniumKeys.NUMPAD2
    NUMPAD3 = SeleniumKeys.NUMPAD3
    NUMPAD4 = SeleniumKeys.NUMPAD4
    NUMPAD5 = SeleniumKeys.NUMPAD5
    NUMPAD6 = SeleniumKeys.NUMPAD6
    NUMPAD7 = SeleniumKeys.NUMPAD7
    NUMPAD8 = SeleniumKeys.NUMPAD8
    NUMPAD9 = SeleniumKeys.NUMPAD9
    MULTIPLY = SeleniumKeys.MULTIPLY
    ADD = SeleniumKeys.ADD
    SEPARATOR = SeleniumKeys.SEPARATOR
    SUBTRACT = SeleniumKeys.SUBTRACT
    DECIMAL = SeleniumKeys.DECIMAL
    DIVIDE = SeleniumKeys.DIVIDE

    F1 = SeleniumKeys.F1
    F2 = SeleniumKeys.F2
    F3 = SeleniumKeys.F3
    F4 = SeleniumKeys.F4
    F5 = SeleniumKeys.F5
    F6 = SeleniumKeys.F6
    F7 = SeleniumKeys.F7
    F8 = SeleniumKeys.F8
    F9 = SeleniumKeys.F9
    F10 = SeleniumKeys.F10
    F11 = SeleniumKeys.F11
    F12 = SeleniumKeys.F12

    META = SeleniumKeys.META
    LEFT_META = META
    RIGHT_META = SeleniumKeys.RIGHT_META
    COMMAND = SeleniumKeys.COMMAND
    LEFT_COMMAND = COMMAND
    ZENKAKU_HANKAKU = SeleniumKeys.ZENKAKU_HANKAKU

    # Extended macOS keys
    LEFT_OPTION = LEFT_ALT
    RIGHT_OPTION = RIGHT_ALT

class BrowserHandler:
    # noinspection PyTypeChecker
    def __init__(self, headless: bool = False):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager(url = "https://msedgedriver.microsoft.com",
            latest_release_url = "https://msedgedriver.microsoft.com/LATEST_RELEASE",).install()),
            options=options
        )

        self.pointer = PointerActions()
        self._network: NetworkHandler = None

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, value: NetworkHandler):
        self._network = value
        self._network.driver = self.driver

    @toolcall
    def navigate(self, url: str):
        """
        navigates to the specified URL.
        :param url: url to navigate to.
        :return: None
        """
        self.driver.get(url)
        self.wait().until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @toolcall
    def reload(self):
        """
        reloads the current page.
        :return: None
        """
        self.driver.refresh()

    @toolcall
    def go_back(self):
        """
        goes to the previous page in history.
        :return: None
        """
        self.driver.back()

    @toolcall
    def go_forward(self):
        """
        goes to the next page in history.
        :return: None
        """
        self.driver.forward()

    @toolcall
    def click(self, selector: str):
        """
        clicks on the first matching element.
        :param selector: CSS selector for the target element.
        :return: None
        """
        self.pointer.click(self.find(selector))

    @toolcall
    def double_click(self, selector: str):
        """
        double-clicks the element.
        :param selector: CSS selector for the target element.
        :return: None
        """
        self.pointer.double_click(self.find(selector))

    @toolcall
    def right_click(self, selector: str):
        """
        right-clicks the element
        :param selector: CSS selector for the target element.
        :return: None
        """
        self.pointer.context_click(self.find(selector))

    @toolcall
    def input_text(self, selector: str, text: str):
        """
        types text into an input field.
        :param selector: CSS selector for the target element.
        :param text: The text to input into the element.
        :return: None
        """
        self.find(selector).send_keys(text)

    @toolcall
    def input_clear(self, selector: str):
        """
        clears the input field.
        :param selector: CSS selector for the target element.
        :return: None
        """
        self.find(selector).clear()

    @toolcall
    def submit(self, selector: str):
        """
        submits a form/button.
        :param selector: CSS selector for the target element
        :return: None
        """
        self.find(selector).submit()

    @toolcall
    def hover(self, selector: str):
        """
        hovers over an element.
        :param selector: CSS selector for the target element.
        :return: None
        """
        self.pointer.move_to(element=self.find(selector))

    @toolcall
    def scroll_to(self, selector: str):
        """
        scrolls to the element.
        :param selector: CSS selector for the target element.
        :return: None
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.find(selector))

    @toolcall
    def scroll_by(self, x: int, y: int):
        """
        scrolls by a pixel amount.
        :param x: the pixel amount to scroll on X.
        :param y: the pixel amount to scroll on Y.
        :return: None
        """
        self.driver.execute_script("window.scrollBy(arguments[0], arguments[1])", x, y)

    @toolcall
    def press_key(self, selector: str, key: Keys):
        """
        simulates a keyboard key press.
        :param selector: CSS selector for the target element.
        :param key: a key on the keyboard.
        :return: None
        """
        self.find(selector).send_keys(key.value)

    @toolcall
    def element_exists(self, selector: str) -> bool:
        """
        returns whether the selector matches any element.
        :param selector: CSS selector for the target element.
        :return: bool
        """
        try:
            return self.find(selector) is not None
        except:
            return False

    @toolcall
    def get_text(self, selector: str) -> str:
        """
        returns inner text of the element.
        :param selector: CSS selector for the target element.
        :return: str
        """
        return self.find(selector).text

    @toolcall
    def get_all_text(self) -> str:
        """
        returns all visible text on the page.
        :return: str
        """
        return self.find("body").text


    @toolcall
    def get_html(self) -> str:
        """
        returns the full page HTML
        :return: str
        """
        return self.driver.page_source

    @toolcall
    def get_outer_html(self, selector: str) -> str:
        """
        returns outer HTML of an element
        :param selector: CSS selector for the target element.
        :return: str
        """
        return self.find(selector).get_attribute("outerHTML")

    @toolcall
    def get_attr(self, selector: str, attribute: str) -> str:
        """
        returns a specific attribute (e.g., href, src).
        :param selector: CSS selector for the target element.
        :param attribute: the attribute to get on the element.
        :return: str
        """
        return self.find(selector).get_attribute(attribute)

    @toolcall
    def get_value(self, selector: str) -> str:
        """
        returns value of an input field
        :param selector: CSS selector for the target element.
        :return: str
        """
        return self.driver.execute_script("""
        if (arguments[0].value != undefined) return arguments[0].value;
        else return arguments[0].innerText;
        """, self.find(selector))

    @toolcall
    def get_tag(self, selector: str) -> str:
        """
        returns the tag name of the element.
        :param selector: CSS selector for the target element.
        :return: str
        """
        return self.find(selector).tag_name

    @toolcall
    def list_links(self) -> List[Dict]:
        """
        returns all <a> tags as {text, href}
        :return: List[Dict]
        """
        links = []

        elms = self.find_all("a", 'tag')

        for element in elms:
            links.append({'text': element.text, 'href': element.get_attribute('href')})

        return links

    @toolcall
    def list_buttons(self) -> List[str]:
        """
        returns all <button> or clickable element selectors.
        :return: List[str]
        """
        result = []
        seen = set()

        for el in self.find_all('button', 'tag'):
            if el.is_displayed() and el.is_enabled():
                html = el.get_attribute('outerHTML')
                if html not in seen:
                    result.append(self.get_element_selector(el))

        for el in self.find_all("//*[@onclick]", "xpath"):
            if el.is_displayed() and el.is_enabled():
                html = el.get_attribute('outerHTML')
                if html not in seen:
                    result.append(self.get_element_selector(el))

        return result

    @toolcall
    def list_inputs(self) -> List[str]:
        """
        returns all <input> and <textarea> element selectors.
        :return:
        """
        result = []
        seen = set()
        for tag in ["input", "textarea"]:
            for el in self.find_all(tag, 'tag'):
                if el.is_displayed() and el.is_enabled():
                    html = el.get_attribute('outerHTML')
                    if html not in seen:
                        result.append(self.get_element_selector(el))
        return result

    @toolcall
    def list_elements(self, selector: str) -> List[str]:
        """
        returns matching element selectors
        :param selector: CSS selector for the target element.
        :return: List[str]
        """
        result = []
        seen = set()

        for el in self.find_all(selector):
            html = el.get_attribute('outerHTML')
            if html not in seen:
                result.append(self.get_element_selector(el))
        return result

    @toolcall
    def select_option(self, selector: str, value: str):
        """
        Selects an <option> inside a <select> by its value attribute.
        :param selector: CSS selector for the target element.
        :param value: value of the option to select.
        :return: None
        """
        # this should be fine?
        # noinspection PyProtectedMember
        _esc = Select._escape_string(None, value)
        opts = self.find(selector).find_elements(by=By.CSS_SELECTOR,value=f"option[value ={_esc}]")

        for opt in opts:
            if not opt.is_selected():
                if not opt.is_enabled():
                    continue
                opt.click()

    @toolcall
    def check(self, selector: str):
        """
        checks a checkbox.
        :param selector: CSS selector for the target element.
        :return: None
        """
        elm = self.find(selector)
        if not elm.is_selected():
            elm.click()

    @toolcall
    def uncheck(self, selector: str):
        """
        unchecks a checkbox.
        :param selector: CSS selector for the target element.
        :return: None
        """
        elm = self.find(selector)
        if elm.is_selected():
            elm.click()

    @toolcall
    def toggle(self, selector: str):
        """
        toggles checkbox/radio/switch.
        :param selector: CSS selector for the target element.
        :return:
        """
        self.click(selector)

    @toolcall
    def set_checkbox(self, selector: str, state: bool):
        """
        sets checkbox to True/False.
        :param selector: CSS selector for the target element.
        :param state: the checkbox state to set it as.
        :return: None
        """
        elm = self.find(selector)
        if state != elm.is_selected():
            elm.click()

    @toolcall
    def wait_for(self, selector: str, timeout: int):
        """
        waits for selector to exist or timeout
        :param selector: CSS selector for the target element.
        :param timeout: The amount of time to wait for selector.
        :return:
        """
        self.wait(timeout).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    @toolcall
    def wait_until_text(self, selector: str, text: str, timeout: int):
        """
        waits for element to contain text.
        :param selector: CSS selector for the target element.
        :param text: A substring or a regex pattern.
        :param timeout: The amount of time to wait for selector.
        :return:
        """

        try:
            pattern = re.compile(text)
            self.wait(timeout).until(
                lambda d: pattern.fullmatch(
                    d.find_element(By.CSS_SELECTOR, selector).text
                ) is not None
            )
        except:
            self.wait(timeout).until(
                expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)
            )

    def get_element_selector(self, element):
        return self.driver.execute_script("""  
          if (!(arguments[0] instanceof Element)) return null;
          const parts = [];
    
          while (arguments[0] && arguments[0].nodeType === 1) {
            let selector = arguments[0].nodeName.toLowerCase();
            if (arguments[0].id) {
              selector += "#" + CSS.escape(arguments[0].id);
              parts.unshift(selector);
              break;
            } else {
              const siblings = Array.from(arguments[0].parentNode.children)
                .filter(e => e.nodeName === arguments[0].nodeName);
              if (siblings.length > 1) {
                const index = siblings.indexOf(arguments[0]) + 1;
                selector += `:nth-of-type(${index})`;
              }
              parts.unshift(selector);
              arguments[0] = arguments[0].parentNode;
            }
          }
    
          return parts.join(" > ");
        """, element)

    def wait(self, timeout: int = 10):
        return WebDriverWait(self.driver, timeout)

    def find(self, selector: str, by="css") -> WebElement:
        mapping = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "tag": By.TAG_NAME,
        }
        return self.driver.find_element(mapping.get(by, By.CSS_SELECTOR), selector)

    def find_all(self, selector: str, by="css") -> List[WebElement]:
        mapping = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "tag": By.TAG_NAME,
        }
        return self.driver.find_elements(mapping.get(by, By.CSS_SELECTOR), selector)

    def quit(self):
        self.driver.quit()

def annotation_allows_none(annotation) -> bool:
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is Union and type(None) in args:
        return True

    if annotation is None or annotation is type(None):
        return True

    return False

# fix this soon
def toolcalls(mcp: FastMCP, obj, register_under):
    tool_calls = []
    open_ai_type = {
        str: "string",
        int: "number",
        bool: "boolean"
    }

    for spect in inspect.getmembers(obj, predicate=inspect.ismethod):
        attr = spect[1]
        if getattr(attr, "_is_toolcall", False):
            sig = inspect.signature(attr)
            print(attr)
            doc = docstring_parser.parse(attr.__doc__)
            properties = {}
            required = []

            for param in doc.params:
                signature = sig.parameters.get(param.arg_name)
                if signature.default == inspect.Signature.empty:
                    required.append(param.arg_name)
                properties[param.arg_name] = {}

                _null = annotation_allows_none(signature.annotation)

                if issubclass(signature.annotation, Enum):
                    properties[param.arg_name].update({
                        'type': 'string' if not _null else ['string','null'],
                        'enum': [e.name for e in signature.annotation]
                    })
                elif signature.annotation in open_ai_type:
                    properties[param.arg_name].update({
                        'type': open_ai_type[signature.annotation] if not _null else [open_ai_type[signature.annotation], 'null']
                    })
                else:
                    print(f"cannot handle type: {signature.annotation} on argument: {param.arg_name} in: {obj.__class__.__name__}.{attr.__name__}")

                properties[param.arg_name].update({
                    'description': param.description
                })

            mcp.tool(
                attr,
                name=f"{register_under}.{attr.__name__}",
                title=None,
                description=doc.description,
                tags=None,
                enabled=True
            )

            tool_call = {
                'type': 'function',
                'function': {
                    'name': f"{register_under}.{attr.__name__}",
                    'description': doc.description,
                    'parameters': {
                        'type': 'object',
                        'properties': properties,
                        'required': required
                    }
                }
            }
            tool_calls.append(tool_call)

    return tool_calls

# notes
"""
EVENTS = {
        "before_request": "network.beforeRequestSent",
        "response_started": "network.responseStarted",
        "response_completed": "network.responseCompleted",
        "auth_required": "network.authRequired",
        "fetch_error": "network.fetchError",
        "continue_request": "network.continueRequest",
        "continue_auth": "network.continueWithAuth",
    }

    PHASES = {
        "before_request": "beforeRequestSent",
        "response_started": "responseStarted",
        "auth_required": "authRequired",
    }
"""

"""
browser = Driver()
ai.register_toolcalls("browser", browser)
browser.network = NetworkHandler()
ai.register_toolcalls("network", browser.network)
"""
