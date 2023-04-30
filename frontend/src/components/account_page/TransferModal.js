import React, {useEffect, useState} from 'react';
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS} from "../../utils/consts";
import Select from "react-select";
import {prettifyFloat} from "../../utils/prettifyFloat";
import {transferMoney} from "../../http/operationsAPI";

const TransferModal = ({show, setShow, account, accounts, setAccountUpdated, accountUpdated}) => {
    const [accountOptions, setAccountOptions] = useState([])
    const [enteredAmount, setEnteredAmount] = useState("")
    const [enteredAmountError, setEnteredAmountError] = useState("")
    const [chosenAccount, setChosenAccount] = useState(null)
    const [commonError, setCommonError] = useState("")
    const [isLoading, setIsLoading] = useState(false)

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
    }, [accounts])


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
        setChosenAccount(null)
        setCommonError("")
    }

    const handleSave = async () => {
        setIsLoading(true)
        if (!enteredAmount && !chosenAccount) {
            setCommonError("At least one field is not filled")
            return
        }
        if (Number(enteredAmount) > Number(account.balance)) {
            setCommonError("After this operation account balance will go negative")
            return
        }
        try {
            return await transferMoney(account, chosenAccount, Number(enteredAmount))
        } catch (e) {
            setCommonError(`${e.response.data.detail || e}`)
        }
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
                    <Row style={{rowGap: "10px"}}>
                        <Form.Group as={Col}>
                            <Form.Label className="little-text mb-1">Amount</Form.Label>
                            <div
                                className="d-flex justify-content-center align-items-center gap-2"
                            >
                                <Form.Control
                                    value={enteredAmount ? enteredAmount : ''}
                                    onChange={(e) => {
                                        setCommonError("")
                                        handleAmountOnChange(e.target.value)
                                    }}
                                    style={{minWidth: "150px"}}
                                    isInvalid={!!enteredAmountError}
                                />
                                <Form.Control.Feedback type="invalid" tooltip id="invalid-tooltip-transfer">
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
                                        minWidth: "180px"
                                    }),
                                }}
                                options={accountOptions}
                                onChange={(v) => {
                                    setChosenAccount(v["value"])
                                }}
                                onMenuOpen={() => {
                                    setCommonError("")
                                    setEnteredAmountError(null)
                                }}
                            />
                        </Form.Group>
                    </Row>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <div className="w-100 d-flex justify-content-between align-items-center m-0">
                    <p className="m-1" style={{color: INTERFACE_COLORS.RED}}>{commonError}</p>
                    <div className="d-flex gap-2">
                        {isLoading ? <Spinner animation="border" className="mx-4"/> :
                            <>
                        <Button
                            variant="secondary"
                            onClick={handleClose}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={() => {
                                handleSave().then((result) => {
                                    if (result.incomeResponse && result.spendingResponse) {
                                        setAccountUpdated(!accountUpdated)
                                        handleClose()
                                    }
                                }).finally(() => setIsLoading(false))
                            }}
                        >
                            Transfer
                        </Button>
                        </>
                    }
                    </div>
                </div>
            </Modal.Footer>
        </Modal>
    );
};

export default TransferModal;