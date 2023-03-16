import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {OPERATIONS_ROUTE, SPENDING_CATEGORIES} from "../utils/consts";
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import Operation from "./Operation";
import ShowMoreModal from "./ShowMoreModal";

const LastOperationsCard = (props) => {
    const [showModal, setShowModal] = useState(false)
    const [navigateTo, setNavigateTo] = useState(OPERATIONS_ROUTE)
    const [operations, setOperations] = useState(null)
    const [amountOfOperations, setAmountOfOperations] = useState(Number(localStorage.getItem("amountOfOperations")))
    const [isLoading, setIsLoading] = useState(true)
    const [tempAmount, setTempAmount] = useState(5)
    const [errorTempAmount, setErrorTempAmount] = useState("")

    const setAmountOfOperationsLocal = (amount) => {
        setAmountOfOperations(amount)
        localStorage.setItem("amountOfOperations", amount)
    }

    const checkAmountOfOperations = () => {
        setIsLoading(true)
        const amount = Number(localStorage.getItem("amountOfOperations"))
        if ((!Number.isInteger(amount)) || (amount < 1) || (amount > 15)) {
            setAmountOfOperationsLocal(5)
        }
    }


    const uniteOperationsForCard = () => {
        let operationsArray = []
        for (let i = 0; i < amountOfOperations; i++) {
            if (props.data.operations.spendings[i]) {
                operationsArray.push(props.data.operations.spendings[i])
            }
            if (props.data.operations.incomes[i]) {
                operationsArray.push(props.data.operations.incomes[i])
            }
        }
        operationsArray.sort((a, b) => new Date(b["created_at"]) - new Date(a["created_at"]))
        setOperations(operationsArray.slice(0, amountOfOperations))
        setIsLoading(false)
    }

    useEffect(() => {
        checkAmountOfOperations();
        uniteOperationsForCard()
    }, [amountOfOperations])

    const handleCloseModal = () => {
        const amount = Number(tempAmount)
        if ((!Number.isInteger(amount)) || (amount < 1) || (amount > 15)) {
            setErrorTempAmount("Amount of operations must be greater than 1 and less than 15")
        } else {
            setAmountOfOperationsLocal(amount)
            setNavigateTo(OPERATIONS_ROUTE)
            setShowModal(false)
            setErrorTempAmount(null)
        }
    }

    return (
        <MainPageCard navigateto={navigateTo} className="d-flex flex-column gap-3">
            {isLoading
                ?
                <div className="d-flex justify-content-center"><Spinner variant="border"/></div>
                :
                <>
                    <div className="d-flex justify-content-between align-items-center">
                        <b>Last operations</b>
                        <ShowMoreModal
                            setNavigateTo={setNavigateTo}
                            setShowModal={setShowModal}
                            navigateTo={navigateTo}
                            showModal={showModal}
                        >
                            <Modal
                                show={showModal}
                                onHide={() => {
                                    setErrorTempAmount(null);
                                    setShowModal(false);
                                    setNavigateTo(OPERATIONS_ROUTE)
                                }}
                                onShow={() => {
                                    setTempAmount(null)
                                }}
                            >
                                <Modal.Header closeButton>
                                    <Modal.Title>Last operations</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <Form>
                                        <Form.Group controlId="amountOfOperationsInput">
                                            <Row>
                                                <Col>
                                                    <Form.Label className="m-0 mt-1">Enter amount of operations:</Form.Label>
                                                </Col>
                                                <Col>
                                                    <Form.Control
                                                        type="number"
                                                        min={1}
                                                        max={15}
                                                        autoFocus
                                                        onChange={(e) => {
                                                            setTempAmount(Number(e.target.value))
                                                        }}
                                                        isInvalid={errorTempAmount}
                                                        aria-errormessage={errorTempAmount}
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
                        </ShowMoreModal>
                    </div>
                    <div className="w-100 d-flex flex-column gap-1">
                        {operations.map(o =>
                            <Operation
                                key={`${o["category"] ? "spending" : "income"}_${o.id}`}
                                name={o.name}
                                amount={o.amount}
                                amountInAccountCurrency={o["amount_in_account_currency_at_creation"]}
                                currency={o.currency}
                                type={o["category"] ? "spending" : "income"}
                                category={o["category"] ? SPENDING_CATEGORIES[o["category"]].name : o["name"]}
                                date={o["created_at"]}
                                icon={o["category"] ? SPENDING_CATEGORIES[o["category"]].icon : null}
                                account={o["category"] ? o["receipt_account"] : o["replenishment_account"]}
                            />)}
                    </div>
                </>}
        </MainPageCard>
    );
};

export default LastOperationsCard;