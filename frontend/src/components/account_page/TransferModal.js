import React, {useEffect, useState} from 'react';
import {Button, Col, Form, Modal, Row} from "react-bootstrap";
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS} from "../../utils/consts";
import Select from "react-select";
import {prettifyFloat} from "../../utils/prettifyFloat";

const TransferModal = ({show, setShow, account, accounts}) => {
    const [accountOptions, setAccountOptions] = useState([])
    const [enteredAmount, setEnteredAmount] = useState("")
    const [enteredAmountError, setEnteredAmountError] = useState("")

    useEffect(() => {
        let tempAccounts = []
        accounts.forEach((a) => {
            if (a.is_active && a !== account) {
                let newAccount = {}
                newAccount["label"] =
                    <div className="d-flex justify-content-between">
                        <p className="m-0">{`${a["name"] ? a["name"] : 'Unnamed account'} (${ACCOUNT_TYPES[a["type"]].name})`}</p>
                        <p className="m-0">{`${prettifyFloat(a["balance"])} ${CURRENCIES_AND_SYMBOLS[a["currency"]]}`}</p>
                    </div>
                newAccount["value"] = a
                tempAccounts.push(newAccount)
            }
        })
        setAccountOptions(tempAccounts)
    }, [])


    const handleAmountOnChange = (value) => {
        if (Number.isNaN(+value)) {
            return
        }
        if (value.toString().includes('.') && value.split('.')[1].length > 2) {
            return
        }
        if (value && value <= 0) {
            setEnteredAmountError("Amount must be greater than 0")
            return
        }
        if (value >= 1000000000) {
            setEnteredAmountError("Amount of operation is too long")
            return
        }
        setEnteredAmount(value)
        setEnteredAmountError("")
    }

    const handleClose = () => {
        setShow(false)
        setEnteredAmountError("")
        setEnteredAmount("")
    }
    return (
        <Modal
            show={show}
            onHide={handleClose}
            size="lg"
        >
            <Modal.Header
                closeButton
            >
                <Modal.Title>Transfer between accounts</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Amount</Form.Label>
                            <div
                                className="d-flex justify-content-center align-items-center gap-2"
                            >
                                <Form.Control
                                    value={enteredAmount ? enteredAmount : ''}
                                    onChange={(e) => {
                                        handleAmountOnChange(e.target.value)
                                    }}
                                    style={{minWidth: "150px"}}
                                    isInvalid={!!enteredAmountError}
                                />
                                <Form.Control.Feedback type="invalid" tooltip>
                                    {enteredAmountError}
                                </Form.Control.Feedback>
                                <p className="m-0">{CURRENCIES_AND_SYMBOLS[account.currency]}</p>
                            </div>
                        </Form.Group>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">
                                To account
                            </Form.Label>
                            <Select
                                placeholder="Select account..."
                                styles={{
                                    control: (baseStyles, state) => ({
                                        ...baseStyles,
                                        minWidth: "90px"
                                    }),
                                }}
                                options={accountOptions}
                                onChange={(v) => {
                                }}
                                onMenuOpen={() => {
                                    setEnteredAmountError(null)
                                }}
                            />
                        </Form.Group>
                    </Row>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary">
                    Cancel
                </Button>
                <Button>
                    Transfer
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default TransferModal;