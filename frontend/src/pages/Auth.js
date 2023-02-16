import React, {useState} from 'react';
import {useAuth} from "../context/Auth";
import {NavLink, useLocation} from "react-router-dom";
import {LOGIN_ROUTE, REGISTRATION_ROUTE} from "../utils/consts";
import {login, registration} from "../http/userAPI";
import {Button, Card, Container, Form, Row} from "react-bootstrap";

const Auth = () => {
    const location = useLocation()
    const isLogin = location.pathname === LOGIN_ROUTE
    const [email, setEmail] = useState('')
    const [password1, setPassword1] = useState('')
    const [password2, setPassword2] = useState('')
    const {user, setUser} = useAuth()

    const loginClick = async () => {
        const response = await login(email, password1)
        console.log(response)
    }

    const registrationClick = async () => {
        const response = await registration(email, password1, password2)
        console.log(response)
    }


    return (
        <Container
            className="d-flex justify-content-center align-items-center"
            style={{height: window.innerHeight}}
        >
            <Card style={{width: 600}} className="p-5">
                <h2 className="m-auto">{isLogin ? 'Sign in to MoneySaver' : 'Sign up to MoneySaver'}</h2>
                <Form classname="d-flex flex-column">
                    <Form.Control
                        className="mt-3"
                        placeholder="Insert your email..."
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    >
                    </Form.Control>
                    <Form.Control
                        className="mt-3"
                        placeholder="Insert your password..."
                        type="password"
                        value={password1}
                        onChange={e => setPassword1(e.target.value)}
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
                </Form>
            </Card>
        </Container>
    );
};

export default Auth;