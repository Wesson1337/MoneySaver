import React, {useCallback, useContext, useState} from 'react';
import {useAuth} from "../context/Auth";
import {useNavigate} from "react-router-dom";
import {MAIN_PAGE_ROUTE} from "../utils/consts";

const Auth = () => {
    const {user, setUser} = useAuth()
    const navigate = useNavigate()

    const login = () => {
        setUser('fsdjadfsjsfj')
        console.log(user)
    }

    const goToMain = () => {
        navigate(MAIN_PAGE_ROUTE)
    }


    return (
        <div>
            AUTH
            <button onClick={login}>dfjasjdf</button>
            <button onClick={goToMain}>main</button>
        </div>
    );
};

export default Auth;