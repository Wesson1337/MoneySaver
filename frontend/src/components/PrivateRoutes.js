import React from 'react';
import {Navigate, Outlet} from "react-router-dom";
import {LOGIN_ROUTE} from "../utils/consts";
import {useAuth} from "../context/Auth";

const PrivateRoutes = () => {
    const {user} = useAuth()
    return (
        user ? <Outlet/> : <Navigate to={LOGIN_ROUTE}/>
    );
};

export default PrivateRoutes;