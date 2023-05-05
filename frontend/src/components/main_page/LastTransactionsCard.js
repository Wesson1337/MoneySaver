import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {INCOME_CATEGORIES, OPERATIONS_ROUTE, SPENDING_CATEGORIES} from "../../utils/consts";
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import Transaction from "../common/Transaction";
import ShowMoreButton from "../common/ShowMoreButton";

const LastTransactionsCard = (props) => {
    const [showModal, setShowModal] = useState(false)
    const [transactions, setTransactions] = useState(null)
    const [amountOfTransactions, setAmountOfTransactions] = useState(Number(localStorage.getItem("amountOfOperations")))
    const [isLoading, setIsLoading] = useState(true)
    const [tempAmount, setTempAmount] = useState(Number(localStorage.getItem("amountOfOperations")))
    const [errorTempAmount, setErrorTempAmount] = useState("")

    const setAmountOfTransactionsLocal = (amount) => {
        setAmountOfTransactions(amount)
        localStorage.setItem("amountOfOperations", amount)
    }

    const checkAmountOfTransactions = () => {
        setIsLoading(true)
        const amount = Number(localStorage.getItem("amountOfOperations"))
        if ((!Number.isInteger(amount)) || (amount < 1) || (amount > 15)) {
            setAmountOfTransactionsLocal(5)
        }
    }

    const uniteTransactionsForCard = () => {
        let transactionsArray = []
        for (let i = 0; i < amountOfTransactions; i++) {
            if (props.data.operations.spendings[i]) {
                transactionsArray.push(props.data.operations.spendings[i])
            }
            if (props.data.operations.incomes[i]) {
                transactionsArray.push(props.data.operations.incomes[i])
            }
        }
        transactionsArray.sort((a, b) => new Date(b["created_at"]) - new Date(a["created_at"]))
        setTransactions(transactionsArray.slice(0, amountOfTransactions))
        setIsLoading(false)
    }

    useEffect(() => {
        checkAmountOfTransactions();
        uniteTransactionsForCard()
    }, [amountOfTransactions])

    const handleCloseModal = () => {
        const amount = Number(tempAmount)
        if ((!Number.isInteger(amount)) || (amount < 1) || (amount > 15)) {
            setErrorTempAmount("Amount of transactions must be greater than 1 and less than 15")
        } else {
            setAmountOfTransactionsLocal(amount)
            setShowModal(false)
            setErrorTempAmount(null)
        }
    }

    return (
        <MainPageCard navigateto={OPERATIONS_ROUTE} showModal={showModal} className="d-flex flex-column gap-3"
                      style={{height: `calc(75px + ${45.633333 * amountOfTransactions}px)`}}
        >
            {isLoading
                ?
                <div className="d-flex justify-content-center"><Spinner animation="border"/></div>
                :
                <>
                    <div className="d-flex justify-content-between align-items-center">
                        <b>Last transactions</b>
                        <ShowMoreButton
                            setShowModal={setShowModal}
                            showModal={showModal}
                        >
                            <Modal
                                show={showModal}
                                onHide={() => {
                                    setErrorTempAmount(null);
                                    setShowModal(false);
                                }}
                                onShow={() => {
                                    setTempAmount(amountOfTransactions)
                                }}
                            >
                                <Modal.Header closeButton>
                                    <Modal.Title>Last transactions</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <Form>
                                        <Form.Group controlId="amountOfOperationsInput">
                                            <Row>
                                                <Col>
                                                    <Form.Label className="m-0 mt-1">Enter amount of
                                                        operations:</Form.Label>
                                                </Col>
                                                <Col>
                                                    <Form.Control
                                                        type="number"
                                                        min={1}
                                                        max={15}
                                                        autoFocus
                                                        value={tempAmount ? tempAmount : null}
                                                        onChange={(e) => {
                                                            setTempAmount(Number(e.target.value))
                                                        }}
                                                        isInvalid={errorTempAmount}
                                                        aria-errormessage={errorTempAmount}
                                                        onKeyDown={(e) => {
                                                            if (e.key === "Enter") {
                                                                e.preventDefault();
                                                                handleCloseModal()
                                                            }
                                                        }}
                                                    >
                                                    </Form.Control>
                                                    <Form.Control.Feedback type="invalid">
                                                        {errorTempAmount}
                                                    </Form.Control.Feedback>
                                                </Col>
                                            </Row>
                                        </Form.Group>
                                    </Form>
                                </Modal.Body>
                                <Modal.Footer>
                                    <Button
                                        variant="primary"
                                        onClick={handleCloseModal}
                                    >
                                        Save changes
                                    </Button>
                                </Modal.Footer>
                            </Modal>
                        </ShowMoreButton>
                    </div>
                    <div className="w-100 d-flex flex-column gap-1">
                        {transactions.map((t, index) =>
                            <Transaction
                                key={`operation-${index}`}
                                amount={t.amount}
                                amountInAccountCurrency={t["amount_in_account_currency_at_creation"]}
                                type={t["receipt_account"] ? "spending" : "income"}
                                category={t["receipt_account"] ? SPENDING_CATEGORIES[t["category"]].name : INCOME_CATEGORIES[t["category"]].name}
                                date={t["created_at"]}
                                icon={t["receipt_account"] ? SPENDING_CATEGORIES[t["category"]].icon : INCOME_CATEGORIES[t["category"]].icon}
                                account={t["receipt_account"] ? t["receipt_account"] : t["replenishment_account"]}
                            />)}
                    </div>
                </>}
        </MainPageCard>
    );
};

export default LastTransactionsCard;