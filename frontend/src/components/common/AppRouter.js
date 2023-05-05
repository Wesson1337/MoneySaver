import React from 'react';
import {Route, Routes} from "react-router-dom";
import PrivateRoutes from "./PrivateRoutes";
import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, TRANSACTIONS_ROUTE, REGISTRATION_ROUTE} from "../../utils/consts";
import MainPage from "../../pages/MainPage";
import Accounts from "../../pages/Accounts";
import Transactions from "../../pages/Transactions";
import Auth from "../../pages/Auth";
import NotFound from "../../pages/NotFound";

const AppRouter = () => {
    return (
        <Routes>
            <Route element={<PrivateRoutes/>}>
                <Route path={MAIN_PAGE_ROUTE} element={<MainPage/>}/>
                <Route path={ACCOUNTS_ROUTE} element={<Accounts/>}/>
                <Route path={TRANSACTIONS_ROUTE} element={<Transactions/>}/>
            </Route>
            <Route path={LOGIN_ROUTE} element={<Auth/>}/>
            <Route path={REGISTRATION_ROUTE} element={<Auth/>}/>
            <Route path="*" element={<NotFound/>}/>
        </Routes>
    );
};

export default AppRouter;