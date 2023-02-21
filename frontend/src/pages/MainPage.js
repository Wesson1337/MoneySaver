import React from 'react';
import {useAuth} from "../context/Auth";

const MainPage = () => {
    const {user} = useAuth()
    return (
        <div>
            <h1>{user}</h1>
            MAIN PAGE
        </div>
    );
};

export default MainPage;