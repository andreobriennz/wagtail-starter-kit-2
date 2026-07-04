'use strict'

// UTILS
function el(selector) {
    return document.querySelector(selector)
}

function toggleClass(element, className) {
    element.classList.toggle(className)
}

function toggleAriaExpanded(element) {
    const currentValue = element.getAttribute('aria-expanded')
    const newValue = currentValue === 'true' ? 'false' : 'true'
    element.setAttribute('aria-expanded', newValue)
}

// only if not using `display: none;`
function toggleTabindex(element) {
    if (element.tabIndex === 0) {
        element.tabIndex = -1
    } else {
        element.tabIndex = 0
    }
}

// COMPONENTS
window.toggleNav = () => {
    const hamburgerIcon = el('#nav-hamburger')
    const navMenu = el('#mobile-nav')

    toggleClass(hamburgerIcon, 'is-active')
    toggleClass(navMenu, 'is-active')
    toggleAriaExpanded(hamburgerIcon)
}

window.handleSearch = function(selector) {
    const query = document.querySelector(selector).value
    window.location.href = '/search?query=' + query
    return false
}

window.showElement = (selector) => {
    const element = el(selector)
    element.style.display = 'block'
}

window.hideElement = (selector) => {
    const element = el(selector)
    element.style.display = 'none'
}

window.focusElement = (selector) => {
    const element = el(selector)
    element.focus()
}

/*
To use this:
Add the [data-accordion-item] HTML attribute around the accordion item.
Then add [data-title] and [data-content] around the title and around the content which will be displayed when the title is clicked.
*/
function watchAccordionItems() {
    const accordionItems = document.querySelectorAll('[data-accordion-item]')
    accordionItems.forEach(item => {
        const title = item.querySelector('[data-title]')
        const content = item.querySelector('[data-content]')

        title.addEventListener('click', () => {
            const downArrow = item.querySelector('.icon-down-arrow')
            toggleClass(content, 'display-none')
            toggleClass(downArrow, 'rotate-180')
        }, { passive: true })
    })
}

// ONLOAD
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.no-js').classList.remove('no-js')

    watchAccordionItems()
}, false)