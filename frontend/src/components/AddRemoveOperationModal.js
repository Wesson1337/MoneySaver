import React, {useState} from 'react';
import {Dropdown, DropdownButton, Modal} from "react-bootstrap";
import {INCOME_CATEGORIES, SPENDING_CATEGORIES} from "../utils/consts";

const AddRemoveOperationModal = ({show, setShow, type}) => {
    const [chosenCategory, setChosenCategory] = useState(null)
    return (
        <>
            <Modal
                show={show}
                onHide={() => {
                    setShow(false)
                }}>
                <Modal.Header closeButton>
                    <Modal.Title>New income</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <DropdownButton id="dropdown-basic-button" title="Choose category">
                        {Object.values(type === "remove" ? SPENDING_CATEGORIES : INCOME_CATEGORIES).map((category) => (
                        <Dropdown.Item
                            key={category.name}
                            onClick={() => {setChosenCategory(category)}}
                        >
                            <div className="d-flex justify-content-between align-items-center gap-3">
                                <img src={category.icon} alt="" height="25px"/>
                                <p className="m-0" style={{minWidth: "145.13px"}}>{category.name}</p>
                            </div>
                        </Dropdown.Item>
                        ))}
                    </DropdownButton>
                </Modal.Body>
            </Modal>
        </>
    );
};

export default AddRemoveOperationModal;