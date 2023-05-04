import React from 'react';
import {Button, Container, Nav, Navbar} from "react-bootstrap";
import dollar from "../../static/icons/dollar-white.svg"
import {useNavigate} from "react-router-dom";
import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE} from "../../utils/consts";
import {useAuth} from "../../context/Auth";
import {logout} from "../../http/userAPI";

const NavBar = () => {
    const navigate = useNavigate()
    const {user, setUser} = useAuth()
    return (
        <>
            <Navbar bg="dark" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand onClick={() => {
                        navigate(MAIN_PAGE_ROUTE)
                    }} style={{cursor: "pointer"}}>
                        <img
                            alt=""
                            src={dollar}
                            width="30"
                            height="30"
                            className="d-inline-block align-top"
                        />{' '}
                        MoneySaver
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="navbarScroll"/>
                    <Navbar.Collapse id="navbarScroll">
                        <Nav
                            className="me-auto my-2 my-lg-0"
                            activeKey={"/" + window.location.pathname.split('/')[1]}
                            navbarScroll
                            style={{maxWidth: "100px"}}
                        >
                            <Nav.Link eventKey={ACCOUNTS_ROUTE}
                                      onClick={() => navigate(ACCOUNTS_ROUTE)}>Accounts</Nav.Link>
                            <Nav.Link eventKey={OPERATIONS_ROUTE}
                                      onClick={() => navigate(OPERATIONS_ROUTE)}>Transactions</Nav.Link>
                        </Nav>
                        {user
                            ?
                            <Button onClick={() => {
                                logout();
                                setUser("");
                                navigate(LOGIN_ROUTE)
                            }} variant="outline-secondary">
                                Sign out
                            </Button>
                            :
                            <Button onClick={() => {
                                navigate(LOGIN_ROUTE)
                            }} variant="outline-secondary">
                                Sign in
                            </Button>
                        }
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </>
    );
};

export default NavBar;