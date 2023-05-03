import React, {useEffect, useState} from 'react';
import {useAuth} from "../context/Auth";
import {NavLink, useLocation, useNavigate} from "react-router-dom";
import {LOGIN_ROUTE, MAIN_PAGE_ROUTE, REGISTRATION_ROUTE} from "../utils/consts";
import {login, registration} from "../http/userAPI";
import {Button, Card, Container, Form, Row, Spinner} from "react-bootstrap";
import {ErrorComponent} from "../components/common/ErrorComponent";

const Auth = () => {
    const navigate = useNavigate()
    const {user, setUser} = useAuth()
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (user) {
            navigate(MAIN_PAGE_ROUTE)
        }
        setLoading(false)
    }, [user, navigate])

    const location = useLocation()
    const isLogin = location.pathname === LOGIN_ROUTE
    const [email, setEmail] = useState('')
    const [password1, setPassword1] = useState('')
    const [password2, setPassword2] = useState('')
    const [errorMsg, setErrorMsg] = useState(null)

    const isValidEmail = () => {
        return /\S+@\S+\.\S+/.test(email)
    }

    const checkEmailAndPassword = () => {
        if (!isValidEmail()) {
            setErrorMsg('Email is incorrect')
            return
        }
        if (password1.length < 6) {
            setErrorMsg('Password should be more than 6 symbols')
            return
        }
        if (!isLogin && (password1 !== password2)) {
            setErrorMsg("Passwords don't match")
            return
        }
        return (isLogin && password1) || (password1 && password2)
    }

    const loginClick = async () => {
        setLoading(true)
        if (checkEmailAndPassword()) {
            try {
                await login(email, password1)
                setUser(email)
                navigate(MAIN_PAGE_ROUTE)
            } catch (e) {
                setErrorMsg(`${e?.response?.data?.detail || e}`)
            }
        }
        setLoading(false)
    }

    const registrationClick = async () => {
        setLoading(true)
        if (checkEmailAndPassword()) {
            try {
                await registration(email, password1, password2)
                setUser(email)
                navigate(MAIN_PAGE_ROUTE)
            } catch (e) {
                setErrorMsg(`${e?.response?.data?.detail || e}`)
            }
        }
        setLoading(false)
    }

    const handleKeyDown = async (e) => {
        if (e.key === 'Enter') {
            isLogin ? await loginClick() : await registrationClick()
        }
    }


    return (
        <Container
            className="d-flex justify-content-center align-items-center"
            style={{height: window.innerHeight - 56}}
        >
            <ErrorComponent
                message={errorMsg}
                onClose={() => setErrorMsg(null)}
            />
            <Card style={{width: 600}} className="p-5">
                <h2 className="m-auto">{isLogin ? 'Sign in to MoneySaver' : 'Sign up to MoneySaver'}</h2>
                {loading ? <Spinner className="m-auto mt-5" animation={"border"}/> :
                    <Form classname="d-flex flex-column">
                        <Form.Control
                            className="mt-3"
                            placeholder="Insert your email..."
                            type="email"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            onKeyDown={handleKeyDown}
                        >
                        </Form.Control>
                        <Form.Control
                            className="mt-3"
                            placeholder="Insert your password..."
                            type="password"
                            value={password1}
                            onChange={e => setPassword1(e.target.value)}
                            onKeyDown={handleKeyDown}
                        >
                        </Form.Control>
                        {isLogin ?
                            '' :
                            <Form.Control
                                className="mt-3"
                                placeholder="Repeat your password..."
                                type="password"
                                value={password2}
                                onChange={e => setPassword2(e.target.value)}
                                onKeyDown={handleKeyDown}
                            >
                            </Form.Control>
                        }
                        <Row className="d-flex justify-content-between mt-3 pl-3 pr-3 gap-3">
                            {isLogin ?
                                <div className="w-auto">
                                    Don't have an account? <NavLink to={REGISTRATION_ROUTE}>Sign up!</NavLink>
                                </div>
                                :
                                <div className="w-auto">
                                    Already have an account? <NavLink to={LOGIN_ROUTE}>Sign in!</NavLink>
                                </div>
                            }
                            <Button
                                className="w-auto"
                                style={{marginRight: 11}}
                                variant={"outline-success"}
                                onClick={isLogin ? loginClick : registrationClick}
                            >
                                {isLogin ? 'Sign in' : 'Sign up'}
                            </Button>
                        </Row>
                    </Form>}
            </Card>
        </Container>
    );
};

export default Auth;