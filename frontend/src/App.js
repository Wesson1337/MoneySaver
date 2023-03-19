import React, {useEffect, useState} from 'react';
import {useAuth} from "./context/Auth";
import {check} from "./http/userAPI";
import {Spinner} from "react-bootstrap";
import NavBar from "./components/NavBar";
import AppRouter from "./components/AppRouter";

function App() {
    const {setUser} = useAuth()
    const [loading, setLoading] = useState(true)
    useEffect(() => {
        check().then(email => {
            setUser(email)
        }).finally(() => setLoading(false))
    }, [])

    return (
        loading ? <Spinner animation='border' style={{position: 'absolute', top: '50%', left: '50%'}}/> :
            <div>
                <NavBar/>
                <AppRouter/>
            </div>
    );
}

export default App;