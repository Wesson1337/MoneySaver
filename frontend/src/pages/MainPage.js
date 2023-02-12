import React from 'react';
import {useAuth} from "../context/Auth";

const MainPage = () => {
    const {user} = useAuth()
    console.log(user)
    return (
        <div>
            MAIN PAGE
        </div>
    );
};

export default MainPage;