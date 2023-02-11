import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE, REGISTRATION_ROUTE} from "./utils/consts";
import MainPage from "./pages/MainPage";
import Auth from "./pages/Auth";
import Accounts from "./pages/Accounts";
import Operations from "./pages/Operations";

export const authRoutes = [
    {
        path: MAIN_PAGE_ROUTE,
        Component: MainPage
    },
    {
        path: ACCOUNTS_ROUTE + '/:id',
        Component: Accounts
    },
    {
        path: OPERATIONS_ROUTE + '/:id',
        Component: Operations
    }
]

export const publicRoutes = [
    {
        path: LOGIN_ROUTE,
        Component: Auth
    },
    {
        path: REGISTRATION_ROUTE,
        Component: Auth
    }
]
