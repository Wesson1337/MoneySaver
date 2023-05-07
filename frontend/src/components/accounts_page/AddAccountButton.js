import React, {useEffect, useState} from 'react';
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS} from "../../utils/consts";
import whitePlusIcon from "../../static/icons/plus-add-create-new-cross-svgrepo-com.svg";
import {Button, Col, Form, Modal, Row, Spinner} from "react-bootstrap";
import Select from "react-select";
import {createAccount} from "../../http/accountsAPI";
import {getUserIdFromJWT} from "../../http/userAPI";
import {handleAmountOnChange} from "../../utils/forms";

const AddAccountButton = ({accountUpdated, setAccountUpdated}) => {
    const [typeOptions, setTypeOptions] = useState([])
    const [showAddModal, setShowAddModal] = useState(false)
    const [chosenType, setChosenType] = useState({})
    const [error, setError] = useState("")
    const [enteredAmount, setEnteredAmount] = useState("")
    const [enteredName, setEnteredName] = useState("")
    const [enteredAmountError, setEnteredAmountError] = useState("")
    const [currencies, setCurrencies] = useState([])
    const [chosenCurrency, setChosenCurrency] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    const handleOnHide = () => {
        setShowAddModal(false)
        setEnteredAmount("")
        setEnteredAmountError("")
        setEnteredName("")
    }

    const handleOnSave = async () => {
        setIsLoading(true)

        if (!enteredName || !chosenType || !chosenCurrency || !enteredAmount) {
            setError("At least one field is not filled")
            return
        }

        try {
            return await createAccount({
                name: enteredName,
                user_id: getUserIdFromJWT(),
                type: chosenType.nameForRequest,
                currency: chosenCurrency,
                balance: enteredAmount
            })
        } catch (e) {
            setError(`${e.response.data.detail || e}`)
        }
    }

    useEffect(() => {
        let tempOptions = []
        Object.values(ACCOUNT_TYPES).forEach((type) => {
            let newType = {}
            newType["label"] =
                <div className="d-flex align-items-center gap-2">
                    <img src={type.icon} alt="" height="25px"/>
                    <p className="m-0"
                       style={{textAlign: "left"}}>{type.name}</p>
                </div>
            newType["value"] = type
            tempOptions.push(newType)
        })
        setTypeOptions(tempOptions)
    }, [])


    useEffect(() => {
        let tempCurrencies = []
        Object.entries(CURRENCIES_AND_SYMBOLS).forEach(([key, value]) => {
            let newCurrency = {label: `${key} - ${value}`, value: key}
            tempCurrencies.push(newCurrency)
        })
        setCurrencies(tempCurrencies)
    }, [])

    return (
        <>
            <div
                className="d-flex flex-column gap-4"
                style={{position: "fixed", bottom: "4%", right: "5%"}}
            >
                <button
                    style={{
                        width: "56px",
                        height: "56px",
                        border: "0px",
                        borderRadius: "50%",
                        background: INTERFACE_COLORS.BLUE
                    }}
                    className="d-flex align-items-center justify-content-center"
                    onClick={() => {
                        setShowAddModal(true)
                    }}
                >
                    <img
                        src={whitePlusIcon}
                        alt=""
                        width="25px"
                    />
                </button>
            </div>
            <Modal
                show={showAddModal}
                onHide={handleOnHide}
                backdrop="static"
                size="lg"
            >
                <Modal.Header closeButton>
                    <Modal.Title>
                        Create new account
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form className="d-flex flex-column gap-3">
                        <Row>
                            <Form.Group as={Col}>
                                <Form.Label className="little-text mb-1">Name</Form.Label>
                                <Form.Control
                                    maxLength={32}
                                    value={enteredName ? enteredName : ""}
                                    onChange={(e) => {
                                        setEnteredName(e.target.value)
                                    }}
                                />
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label className="little-text mb-1">Type</Form.Label>
                                <Select
                                    onMenuOpen={() => {
                                        setError("")
                                    }}
                                    options={typeOptions}
                                    onChange={(v) => setChosenType(v["value"])}
                                />
                            </Form.Group>
                        </Row>
                        <Row>
                            <Form.Group as={Col}>
                                <Form.Label className="little-text mb-1">Initial amount</Form.Label>
                                <Form.Control
                                    value={enteredAmount ? enteredAmount : ''}
                                    onChange={(e) => {
                                        handleAmountOnChange(e.target.value, setEnteredAmount, setEnteredAmountError)
                                        setError("")
                                    }}
                                    style={{minWidth: "150px"}}
                                    isInvalid={!!enteredAmountError}
                                />
                                <Form.Control.Feedback type="invalid">
                                    {enteredAmountError}
                                </Form.Control.Feedback>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label className="little-text mb-1">Currency</Form.Label>
                                <Select
                                    placeholder=""
                                    styles={{
                                        control: (baseStyles, state) => ({
                                            ...baseStyles,
                                            minWidth: "80px"
                                        }),
                                    }}
                                    options={currencies}
                                    onChange={(v) => {
                                        setChosenCurrency(v["value"]);
                                        setError("")
                                    }}
                                />
                            </Form.Group>
                        </Row>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <div className="d-flex justify-content-between align-items-center w-100">
                        <p className="m-0" style={{color: INTERFACE_COLORS.RED}}>{error}</p>
                        {isLoading ? <div className="mx-4"><Spinner animation="border"/></div> :
                            <div className="d-flex gap-2">
                                <Button
                                    variant="secondary"
                                    onClick={handleOnHide}
                                >Close</Button>
                                <Button
                                    onClick={() => {
                                        handleOnSave().then((r) => {
                                            if (r) {
                                                setIsLoading(false)
                                                setAccountUpdated(!accountUpdated)
                                                handleOnHide()
                                            }
                                        }).finally(() => setIsLoading(false))
                                    }}
                                >Save</Button>
                            </div>
                        }
                    </div>
                </Modal.Footer>
            </Modal>
        </>
    );
};

export default AddAccountButton;