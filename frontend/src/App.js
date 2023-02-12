import React from 'react';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import MainPage from "./pages/MainPage";
import Auth from "./pages/Auth";
import PrivateRoutes from "./utils/PrivateRoutes";
import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE, REGISTRATION_ROUTE} from "./utils/consts";
import Accounts from "./pages/Accounts";
import Operations from "./pages/Operations";
import {AuthProvider} from "./context/Auth";

function App() {
  return (
      <AuthProvider>
          <Routes>
              <Route element={<PrivateRoutes/>}>
                  <Route path={MAIN_PAGE_ROUTE} element={<MainPage/>} />
                  <Route path={ACCOUNTS_ROUTE} element={<Accounts/>} />
                  <Route path={OPERATIONS_ROUTE} element={<Operations/>} />
              </Route>
              <Route path={LOGIN_ROUTE} element={<Auth/>}/>
              <Route path={REGISTRATION_ROUTE} element={<Auth/>}/>
          </Routes>
      </AuthProvider>
  );
}

export default App;