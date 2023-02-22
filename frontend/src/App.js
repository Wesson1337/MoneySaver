import React, {useContext, useEffect, useState} from 'react';
import {Route, Routes} from "react-router-dom";
import MainPage from "./pages/MainPage";
import Auth from "./pages/Auth";
import PrivateRoutes from "./utils/PrivateRoutes";
import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE, REGISTRATION_ROUTE} from "./utils/consts";
import Accounts from "./pages/Accounts";
import Operations from "./pages/Operations";
import {useAuth} from "./context/Auth";
import {check} from "./http/userAPI";
import {Spinner} from "react-bootstrap";

function App() {
    const {setUser} = useAuth()
    const [loading, setLoading] = useState(true)
    useEffect(() => {
        check().then(data => {
            setUser(true)
        }).finally(() => setLoading(false))
    }, [])
  return (
      loading ? <Spinner animation='border' style={{position: 'absolute', top: '50%', left: '50%'}}/> :
          <Routes>
              <Route element={<PrivateRoutes/>}>
                  <Route path={MAIN_PAGE_ROUTE} element={<MainPage/>} />
                  <Route path={ACCOUNTS_ROUTE} element={<Accounts/>} />
                  <Route path={OPERATIONS_ROUTE} element={<Operations/>} />
              </Route>
              <Route path={LOGIN_ROUTE} element={<Auth/>}/>
              <Route path={REGISTRATION_ROUTE} element={<Auth/>}/>
          </Routes>
  );
}

export default App;