/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./packages/nhsuk.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/nhsuk-frontend/packages/common.js":
/*!********************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/common.js ***!
  \********************************************************/
/*! exports provided: toggleAttribute, toggleConditionalInput */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"toggleAttribute\", function() { return toggleAttribute; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"toggleConditionalInput\", function() { return toggleConditionalInput; });\n/**\n * Toggle a boolean attribute on a HTML element\n * @param {HTMLElement} element\n * @param {string} attr\n*/\nvar toggleAttribute = function toggleAttribute(element, attr) {\n  // Return without error if element or attr are missing\n  if (!element || !attr) return; // Toggle attribute value. Treat no existing attr same as when set to false\n\n  var value = element.getAttribute(attr) === 'true' ? 'false' : 'true';\n  element.setAttribute(attr, value);\n};\n/**\n * Toggle a toggle a class on conditional content for an input based on checked state\n * @param {HTMLElement} input input element\n * @param {string} className class to toggle\n*/\n\nvar toggleConditionalInput = function toggleConditionalInput(input, className) {\n  // Return without error if input or class are missing\n  if (!input || !className) return; // If the input has conditional content it had a data-aria-controls attribute\n\n  var conditionalId = input.getAttribute('aria-controls');\n\n  if (conditionalId) {\n    // Get the conditional element from the input data-aria-controls attribute\n    var conditionalElement = document.getElementById(conditionalId);\n\n    if (conditionalElement) {\n      conditionalElement.classList.toggle(className);\n      toggleAttribute(input, 'aria-expanded');\n    }\n  }\n};\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/common.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/card/card.js":
/*!**********************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/card/card.js ***!
  \**********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // Loops through dom and finds all elements with nhsuk-card--clickable class\n  document.querySelectorAll('.nhsuk-card--clickable').forEach(function (card) {\n    // Check if card has a link within it\n    if (card.querySelector('a') !== null) {\n      // Clicks the link within the heading to navigate to desired page\n      card.addEventListener('click', function () {\n        card.querySelector('a').click();\n      });\n    }\n  });\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/card/card.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/checkboxes/checkboxes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/checkboxes/checkboxes.js ***!
  \**********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common */ \"./node_modules/nhsuk-frontend/packages/common.js\");\n\n/**\n * Conditionally show content when a checkbox button is checked\n * Test at http://0.0.0.0:3000/components/checkboxes/conditional.html\n*/\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // Checkbox input DOMElements inside a conditional form group\n  var checkboxInputs = document.querySelectorAll('.nhsuk-checkboxes--conditional .nhsuk-checkboxes__input');\n  /**\n   * Toggle classes and attributes\n   * @param {Object} event click event object\n  */\n\n  var handleClick = function handleClick(event) {\n    // Toggle conditional content based on checked state\n    Object(_common__WEBPACK_IMPORTED_MODULE_0__[\"toggleConditionalInput\"])(event.target, 'nhsuk-checkboxes__conditional--hidden');\n  }; // Attach handleClick as click to checkboxInputs\n\n\n  checkboxInputs.forEach(function (checkboxButton) {\n    checkboxButton.addEventListener('change', handleClick);\n  });\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/checkboxes/checkboxes.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/details/details.js":
/*!****************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/details/details.js ***!
  \****************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common */ \"./node_modules/nhsuk-frontend/packages/common.js\");\n\n/**\n * Ensure details component is cross browser and accessible\n * Test at http://0.0.0.0:3000/components/details/index.html\n*/\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // Does the browser support details component\n  var nativeSupport = typeof document.createElement('details').open === 'boolean'; // Nodelist of all details elements\n\n  var allDetails = document.querySelectorAll('details');\n  /**\n   * Adds all necessary functionality to a details element\n   * @param {HTMLElement} element details element to initialise\n   * @param {number} index number to be appended to dynamic IDs\n  */\n\n  var initDetails = function initDetails(element, index) {\n    // Set details element as polyfilled to prevent duplicate events being added\n    element.setAttribute('nhsuk-polyfilled', 'true'); // Give details element an ID if it doesn't already have one\n\n    if (!element.id) element.setAttribute('id', \"nhsuk-details\".concat(index)); // Set content element and give it an ID if it doesn't already have one\n\n    var content = document.querySelector(\"#\".concat(element.id, \" .nhsuk-details__text\"));\n    if (!content.id) content.setAttribute('id', \"nhsuk-details__text\".concat(index)); // Set summary element\n\n    var summary = document.querySelector(\"#\".concat(element.id, \" .nhsuk-details__summary\")); // Set initial summary aria attributes\n\n    summary.setAttribute('role', 'button');\n    summary.setAttribute('aria-controls', content.id);\n    summary.setAttribute('tabIndex', '0');\n    var openAttr = element.getAttribute('open') !== null;\n\n    if (openAttr === true) {\n      summary.setAttribute('aria-expanded', 'true');\n      content.setAttribute('aria-hidden', 'false');\n    } else {\n      summary.setAttribute('aria-expanded', 'false');\n      content.setAttribute('aria-hidden', 'true'); // Hide content on browsers without native details support\n\n      if (!nativeSupport) content.style.display = 'none';\n    }\n\n    var toggleDetails = function toggleDetails() {\n      Object(_common__WEBPACK_IMPORTED_MODULE_0__[\"toggleAttribute\"])(summary, 'aria-expanded');\n      Object(_common__WEBPACK_IMPORTED_MODULE_0__[\"toggleAttribute\"])(content, 'aria-hidden');\n\n      if (!nativeSupport) {\n        content.style.display = content.getAttribute('aria-hidden') === 'true' ? 'none' : '';\n\n        if (element.hasAttribute('open')) {\n          element.removeAttribute('open');\n        } else {\n          element.setAttribute('open', 'open');\n        }\n      }\n    }; // Toggle details onclick\n\n\n    summary.addEventListener('click', toggleDetails); // Call toggle details on enter and space key events\n\n    summary.addEventListener('keydown', function (event) {\n      if (event.keyCode === 13 || event.keyCode === 32) {\n        event.preventDefault();\n        summary.click();\n      }\n    });\n  }; // Initialise details for any new details element\n\n\n  if (allDetails.length) {\n    allDetails.forEach(function (element, index) {\n      if (!element.hasAttribute('nhsuk-polyfilled')) initDetails(element, index);\n    });\n  }\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/details/details.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/error-summary/error-summary.js":
/*!****************************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/error-summary/error-summary.js ***!
  \****************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/**\n * Adapted from https://github.com/alphagov/govuk-frontend/blob/master/src/govuk/components/error-summary/error-summary.js\n */\n\n/**\n * Get associated legend or label\n *\n * Returns the first element that exists from this list:\n *\n * - The `<legend>` associated with the closest `<fieldset>` ancestor, as long\n *   as the top of it is no more than half a viewport height away from the\n *   bottom of the input\n * - The first `<label>` that is associated with the input using for='inputId'\n * - The closest parent `<label>`\n */\nfunction getAssociatedLegendOrLabel(input) {\n  var fieldset = input.closest('fieldset');\n\n  if (fieldset) {\n    var legends = fieldset.getElementsByTagName('legend');\n\n    if (legends.length) {\n      var candidateLegend = legends[0]; // eslint-disable-line prefer-destructuring\n      // If the input type is radio or checkbox, always use the legend if there\n      // is one.\n\n      if (input.type === 'checkbox' || input.type === 'radio') {\n        return candidateLegend;\n      } // For other input types, only scroll to the fieldset’s legend (instead of\n      // the label associated with the input) if the input would end up in the\n      // top half of the screen.\n      //\n      // This should avoid situations where the input either ends up off the\n      // screen, or obscured by a software keyboard.\n\n\n      var legendTop = candidateLegend.getBoundingClientRect().top;\n      var inputRect = input.getBoundingClientRect(); // If the browser doesn't support Element.getBoundingClientRect().height\n      // or window.innerHeight (like IE8), bail and just link to the label.\n\n      if (inputRect.height && window.innerHeight) {\n        var inputBottom = inputRect.top + inputRect.height;\n\n        if (inputBottom - legendTop < window.innerHeight / 2) {\n          return candidateLegend;\n        }\n      }\n    }\n  }\n\n  return document.querySelector(\"label[for='\".concat(input.getAttribute('id'), \"']\")) || input.closest('label');\n}\n/**\n * Focus the target element\n *\n * By default, the browser will scroll the target into view. Because our labels\n * or legends appear above the input, this means the user will be presented with\n * an input without any context, as the label or legend will be off the top of\n * the screen.\n *\n * Manually handling the click event, scrolling the question into view and then\n * focussing the element solves this.\n *\n * This also results in the label and/or legend being announced correctly in\n * NVDA - without this only the field type is announced\n * (e.g. 'Edit, has autocomplete').\n */\n\n\nfunction focusTarget(target) {\n  // If the element that was clicked was not a link, return early\n  if (target.tagName !== 'A' || target.href === false) {\n    return false;\n  }\n\n  var input = document.querySelector(target.hash);\n\n  if (!input) {\n    return false;\n  }\n\n  var legendOrLabel = getAssociatedLegendOrLabel(input);\n\n  if (!legendOrLabel) {\n    return false;\n  } // Scroll the legend or label into view *before* calling focus on the input to\n  // avoid extra scrolling in browsers that don't support `preventScroll` (which\n  // at time of writing is most of them...)\n\n\n  legendOrLabel.scrollIntoView();\n  input.focus({\n    preventScroll: true\n  });\n  return true;\n}\n/**\n * Handle click events on the error summary\n */\n\n\nfunction handleClick(event) {\n  if (focusTarget(event.target)) {\n    event.preventDefault();\n  }\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // Error summary component\n  var errorSummary = document.querySelector('.nhsuk-error-summary');\n\n  if (errorSummary) {\n    // Focus error summary component if it exists\n    errorSummary.focus();\n    errorSummary.addEventListener('click', handleClick);\n  }\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/error-summary/error-summary.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/header/header.js":
/*!**************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/header/header.js ***!
  \**************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _menuToggle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./menuToggle */ \"./node_modules/nhsuk-frontend/packages/components/header/menuToggle.js\");\n/* harmony import */ var _searchToggle__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./searchToggle */ \"./node_modules/nhsuk-frontend/packages/components/header/searchToggle.js\");\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  Object(_menuToggle__WEBPACK_IMPORTED_MODULE_0__[\"default\"])();\n  Object(_searchToggle__WEBPACK_IMPORTED_MODULE_1__[\"default\"])();\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/header/header.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/header/menuToggle.js":
/*!******************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/header/menuToggle.js ***!
  \******************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common */ \"./node_modules/nhsuk-frontend/packages/common.js\");\n\n/**\n * Handle menu show and hide for mobile\n*/\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // HTMLElements\n  var toggleButton = document.querySelector('#toggle-menu');\n  var closeButton = document.querySelector('#close-menu');\n  var nav = document.querySelector('#header-navigation');\n  /**\n   * Toggle classes and attributes\n   * @param {Object} event click event object\n  */\n\n  var toggleMenu = function toggleMenu(event) {\n    event.preventDefault(); // Toggle aria-expanded for accessibility\n\n    Object(_common__WEBPACK_IMPORTED_MODULE_0__[\"toggleAttribute\"])(toggleButton, 'aria-expanded'); // Toggle classes to apply CSS\n\n    toggleButton.classList.toggle('is-active');\n    nav.classList.toggle('js-show');\n  }; // Check all necessary HTMLElements exist\n\n\n  if (toggleButton && closeButton && nav) {\n    // Attach toggleMenu as click to any elements which need it\n    [toggleButton, closeButton].forEach(function (elem) {\n      elem.addEventListener('click', toggleMenu);\n    });\n  }\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/header/menuToggle.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/header/searchToggle.js":
/*!********************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/header/searchToggle.js ***!
  \********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common */ \"./node_modules/nhsuk-frontend/packages/common.js\");\n\n/**\n * Handle search show and hide for mobile\n*/\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // HTMLElements\n  var toggleButton = document.querySelector('#toggle-search');\n  var closeButton = document.querySelector('#close-search');\n  var searchContainer = document.querySelector('#wrap-search');\n  var menuSearchContainer = document.querySelector('#content-header');\n  /**\n   * Toggle classes and attributes\n   * @param {Object} event click event object\n  */\n\n  var toggleSearch = function toggleSearch(event) {\n    event.preventDefault(); // Toggle aria-expanded for accessibility\n\n    Object(_common__WEBPACK_IMPORTED_MODULE_0__[\"toggleAttribute\"])(toggleButton, 'aria-expanded'); // Toggle classes to apply CSS\n\n    toggleButton.classList.toggle('is-active');\n    searchContainer.classList.toggle('js-show');\n    menuSearchContainer.classList.toggle('js-show');\n  }; // Check all necessary HTMLElements exist\n\n\n  if (toggleButton && closeButton) {\n    // Attach toggleSearch as click to any elements which need it\n    [toggleButton, closeButton].forEach(function (elem) {\n      elem.addEventListener('click', toggleSearch);\n    });\n  }\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/header/searchToggle.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/radios/radios.js":
/*!**************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/radios/radios.js ***!
  \**************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../common */ \"./node_modules/nhsuk-frontend/packages/common.js\");\n\n/**\n * Conditionally show content when a radio button is checked\n * Test at http://0.0.0.0:3000/components/radios/conditional.html\n*/\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // Radio input HTMLElements inside a conditional form group\n  var radioInputs = document.querySelectorAll('.nhsuk-radios--conditional .nhsuk-radios__input'); // Conditional content inside a conditional form group\n\n  var conditionalInputs = document.querySelectorAll('.nhsuk-radios--conditional .nhsuk-radios__conditional');\n  /**\n   * Toggle classes and attributes\n   * @param {Object} event click event object\n  */\n\n  var handleClick = function handleClick(event) {\n    // Hide all conditional content on all input clicks\n    radioInputs.forEach(function (input) {\n      return input.setAttribute('aria-expanded', 'false');\n    });\n    conditionalInputs.forEach(function (input) {\n      return input.classList.add('nhsuk-radios__conditional--hidden');\n    }); // Toggle conditional content based on checked state\n\n    Object(_common__WEBPACK_IMPORTED_MODULE_0__[\"toggleConditionalInput\"])(event.target, 'nhsuk-radios__conditional--hidden');\n  }; // Attach handleClick as click to radioInputs\n\n\n  radioInputs.forEach(function (radioButton) {\n    radioButton.addEventListener('change', handleClick);\n  });\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/radios/radios.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/components/skip-link/skip-link.js":
/*!********************************************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/components/skip-link/skip-link.js ***!
  \********************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/*\n * NHS.UK skip link.\n *\n * When using VoiceOver on iOS, focus remains on the skip link anchor\n * when elected so the next focusable element is not at the jumped to area.\n */\n/* harmony default export */ __webpack_exports__[\"default\"] = (function () {\n  // Assign required DOM elements\n  var heading = document.querySelector('h1');\n  var skipLink = document.querySelector('.nhsuk-skip-link');\n\n  var addEvents = function addEvents() {\n    // Add tabindex = -1 and apply focus to heading on skip link click\n    skipLink.addEventListener('click', function (event) {\n      event.preventDefault();\n      heading.setAttribute('tabIndex', '-1');\n      heading.focus();\n    }); // Remove tabindex from heading on blur\n\n    heading.addEventListener('blur', function (event) {\n      event.preventDefault();\n      heading.removeAttribute('tabIndex');\n    });\n  };\n\n  if (heading && skipLink) addEvents();\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/components/skip-link/skip-link.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/nhsuk.js":
/*!*******************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/nhsuk.js ***!
  \*******************************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _components_card_card__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components/card/card */ \"./node_modules/nhsuk-frontend/packages/components/card/card.js\");\n/* harmony import */ var _components_checkboxes_checkboxes__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/checkboxes/checkboxes */ \"./node_modules/nhsuk-frontend/packages/components/checkboxes/checkboxes.js\");\n/* harmony import */ var _components_details_details__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/details/details */ \"./node_modules/nhsuk-frontend/packages/components/details/details.js\");\n/* harmony import */ var _components_error_summary_error_summary__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/error-summary/error-summary */ \"./node_modules/nhsuk-frontend/packages/components/error-summary/error-summary.js\");\n/* harmony import */ var _components_header_header__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/header/header */ \"./node_modules/nhsuk-frontend/packages/components/header/header.js\");\n/* harmony import */ var _components_radios_radios__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/radios/radios */ \"./node_modules/nhsuk-frontend/packages/components/radios/radios.js\");\n/* harmony import */ var _components_skip_link_skip_link__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/skip-link/skip-link */ \"./node_modules/nhsuk-frontend/packages/components/skip-link/skip-link.js\");\n/* harmony import */ var _polyfills__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./polyfills */ \"./node_modules/nhsuk-frontend/packages/polyfills.js\");\n/* harmony import */ var _polyfills__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_polyfills__WEBPACK_IMPORTED_MODULE_7__);\n// Components\n\n\n\n\n\n\n\n // Initialize components\n\ndocument.addEventListener('DOMContentLoaded', function () {\n  Object(_components_card_card__WEBPACK_IMPORTED_MODULE_0__[\"default\"])();\n  Object(_components_checkboxes_checkboxes__WEBPACK_IMPORTED_MODULE_1__[\"default\"])();\n  Object(_components_details_details__WEBPACK_IMPORTED_MODULE_2__[\"default\"])();\n  Object(_components_error_summary_error_summary__WEBPACK_IMPORTED_MODULE_3__[\"default\"])();\n  Object(_components_header_header__WEBPACK_IMPORTED_MODULE_4__[\"default\"])();\n  Object(_components_radios_radios__WEBPACK_IMPORTED_MODULE_5__[\"default\"])();\n  Object(_components_skip_link_skip_link__WEBPACK_IMPORTED_MODULE_6__[\"default\"])();\n});\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/nhsuk.js?");

/***/ }),

/***/ "./node_modules/nhsuk-frontend/packages/polyfills.js":
/*!***********************************************************!*\
  !*** ./node_modules/nhsuk-frontend/packages/polyfills.js ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("/**\n * IE polyfill for NodeList.forEach()\n */\nif (!NodeList.prototype.forEach) {\n  NodeList.prototype.forEach = Array.prototype.forEach;\n}\n/**\n * IE polyfill for Array.includes()\n */\n\n\nif (!Array.prototype.includes) {\n  // eslint-disable-next-line no-extend-native\n  Object.defineProperty(Array.prototype, 'includes', {\n    enumerable: false,\n    value: function value(obj) {\n      return this.filter(function (el) {\n        return el === obj;\n      }).length > 0;\n    }\n  });\n}\n/**\n * IE polyfill for Element.closest()\n */\n\n\nif (!Element.prototype.matches) {\n  Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector;\n}\n\nif (!Element.prototype.closest) {\n  Element.prototype.closest = function (s) {\n    var el = this;\n\n    do {\n      if (Element.prototype.matches.call(el, s)) return el;\n      el = el.parentElement || el.parentNode;\n    } while (el !== null && el.nodeType === 1);\n\n    return null;\n  };\n}\n\n//# sourceURL=webpack:///./node_modules/nhsuk-frontend/packages/polyfills.js?");

/***/ }),

/***/ "./packages/mega-menu-toggle.js":
/*!**************************************!*\
  !*** ./packages/mega-menu-toggle.js ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("document.getElementById(\"toggle-menu\").addEventListener(\"click\", function (e) {\n  e.preventDefault();\n  var nav = document.getElementById(\"mega-menu\");\n  nav.style.display = nav.style.display === 'block' ? 'none' : 'block';\n}, false);\n\n//# sourceURL=webpack:///./packages/mega-menu-toggle.js?");

/***/ }),

/***/ "./packages/nhsuk.js":
/*!***************************!*\
  !*** ./packages/nhsuk.js ***!
  \***************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _node_modules_nhsuk_frontend_packages_nhsuk__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/nhsuk-frontend/packages/nhsuk */ \"./node_modules/nhsuk-frontend/packages/nhsuk.js\");\n/* harmony import */ var _search_toggle_fix__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./search-toggle-fix */ \"./packages/search-toggle-fix.js\");\n/* harmony import */ var _search_toggle_fix__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_search_toggle_fix__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _mega_menu_toggle__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./mega-menu-toggle */ \"./packages/mega-menu-toggle.js\");\n/* harmony import */ var _mega_menu_toggle__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mega_menu_toggle__WEBPACK_IMPORTED_MODULE_2__);\n\n //for issue https://github.com/rkhleics/nhs-ei.website/issues/29\n\n //for issue https://github.com/rkhleics/nhs-ei.website/issues/29\n\n//# sourceURL=webpack:///./packages/nhsuk.js?");

/***/ }),

/***/ "./packages/search-toggle-fix.js":
/*!***************************************!*\
  !*** ./packages/search-toggle-fix.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("/**\n * for issue https://github.com/rkhleics/nhs-ei.website/issues/29\n * a patch to make the search button work\n * we won't need this going forward but it needs to remain in place for now\n * until the wagtailfrontend package is no longer used\n * an altertanive is to use the header includes from wagtailfrontend package that has\n * been altered to allow this to work when its used but not for now.\n */\nvar searchBar = document.querySelector('.nhsuk-header__search');\n\nif (searchBar) {\n  var toggleButton = document.querySelector('#toggle-search');\n  var closeButton = document.querySelector('#close-search');\n  var searchContainer = document.querySelector('#wrap-search');\n  var menuSearchContainer = document.querySelector('#content-header');\n  toggleButton.addEventListener('click', function () {\n    toggleButton.setAttribute('aria-expanded', true);\n    toggleButton.classList.add('is-active');\n    searchContainer.classList.add('js-show');\n    menuSearchContainer.classList.add('js-show');\n  });\n  closeButton.addEventListener('click', function () {\n    toggleButton.removeAttribute('aria-expanded');\n    toggleButton.classList.remove('is-active');\n    searchContainer.classList.remove('js-show');\n    menuSearchContainer.classList.remove('js-show');\n  });\n}\n/** end */\n\n//# sourceURL=webpack:///./packages/search-toggle-fix.js?");

/***/ })

/******/ });