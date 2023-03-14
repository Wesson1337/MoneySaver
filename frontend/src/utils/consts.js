import supermarketIcon from '../static/icons/categories_icons/supermarket-svgrepo-com.svg'
import transferIcon from '../static/icons/categories_icons/transfer-fee-svgrepo-com.svg'
import fastFoodIcon from '../static/icons/categories_icons/fastfood-svgrepo-com.svg'
import taxiIcon from '../static/icons/categories_icons/taxi-svgrepo-com.svg'
import entertainmentIcon from '../static/icons/categories_icons/entertainment-svgrepo-com.svg'
import miscellaneousIcon from '../static/icons/categories_icons/miscellaneous-collection-svgrepo-com.svg'
import transportIcon from '../static/icons/categories_icons/transport-svgrepo-com.svg'
import serviceIcon from '../static/icons/categories_icons/corp-purchase-svgrepo-com.svg'
import pharmaciesIcon from '../static/icons/categories_icons/pharmacy-svgrepo-com.svg'
import billsIcon from '../static/icons/categories_icons/business-expense-svgrepo-com.svg'
import clothingIcon from '../static/icons/categories_icons/clothing-svgrepo-com.svg'
import beautyIcon from '../static/icons/categories_icons/cosmetics-svgrepo-com.svg'
import homeImprovementIcon from '../static/icons/categories_icons/home-svgrepo-com.svg'
import otherIcon from '../static/icons/categories_icons/other-income-svgrepo-com.svg'

export const LOGIN_ROUTE = '/login'
export const REGISTRATION_ROUTE = '/registration'
export const MAIN_PAGE_ROUTE = '/'
export const ACCOUNTS_ROUTE = '/accounts'
export const OPERATIONS_ROUTE = '/operations'

export const SUPPORTED_CURRENCIES = {
    USD: 'USD',
    RUB: 'RUB',
    CNY: 'CNY',
    EUR: 'EUR',
    GBP: 'GBP',
    CAD: 'CAD'
}

export const CURRENCIES_AND_SYMBOLS = {
    USD: "$",
    RUB: "₽",
    CNY: "¥",
    EUR: "€",
    GBP: "£",
    CAD: "C$"
}

export const GREEN = "#428345"
export const RED = "#d93838"

export const SPENDING_CATEGORIES = {
    SUPERMARKETS: {
        name: "Supermarkets",
        nameForRequest: "SUPERMARKETS",
        icon: supermarketIcon
    },
    TRANSFERS: {
        name: "Transfers",
        nameForRequest: "TRANSFERS",
        icon: transferIcon
    },
    FAST_FOOD: {
        name: "Fast Food",
        nameForRequest: "FAST_FOOD",
        icon: fastFoodIcon
    },
    TAXI: {
        name: "Taxi",
        nameForRequest: "TAXI",
        icon: taxiIcon
    },
    ENTERTAINMENT: {
        name: "Entertainment",
        nameForRequest: "ENTERTAINMENT",
        icon: entertainmentIcon
    },
    MISCELLANEOUS: {
        name: "Miscellaneous",
        nameForRequest: "MISCELLANEOUS",
        icon: miscellaneousIcon
    },
    TRANSPORT: {
        name: "Transport",
        nameForRequest: "TRANSPORT",
        icon: transportIcon
    },
    SERVICE: {
        name: "Service",
        nameForRequest: "SERVICE",
        icon: serviceIcon
    },
    PHARMACIES: {
        name: "Pharmacies",
        nameForRequest: "PHARMACIES",
        icon: pharmaciesIcon
    },
    BILLS: {
        name: "Bills",
        nameForRequest: "BILLS",
        icon: billsIcon
    },
    CLOTHING: {
        name: "Clothing",
        nameForRequest: "CLOTHING",
        icon: clothingIcon
    },
    BEAUTY: {
        name: "Beauty",
        nameForRequest: "BEAUTY",
        icon: beautyIcon
    },
    HOME_IMPROVEMENT: {
        name: "Home Improvement",
        nameForRequest: "HOME_IMPROVEMENT",
        icon: homeImprovementIcon
    },
    OTHER: {
        name: "Other",
        nameForRequest: "OTHER",
        icon: otherIcon
    }
}