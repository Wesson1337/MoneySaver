import React, {useState} from 'react';
import {Dropdown, DropdownButton, Modal} from "react-bootstrap";
import {SPENDING_CATEGORIES} from "../utils/consts";

const AddRemoveModal = ({show, setShow}) => {
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
                        {Object.keys(SPENDING_CATEGORIES).map((category) => (
                        <Dropdown.Item
                            key={category}
                            onClick={() => {setChosenCategory(SPENDING_CATEGORIES[category])}}
                        >
                            <div className="d-flex justify-content-between align-items-center gap-3">
                                <img src={SPENDING_CATEGORIES[category].icon} alt="" height="25px"/>
                                <p className="m-0" style={{minWidth: "145.13px"}}>{SPENDING_CATEGORIES[category].name}</p>
                            </div>
                        </Dropdown.Item>
                        ))}
                    </DropdownButton>
                </Modal.Body>
            </Modal>
        </>
    );
};

export default AddRemoveModal;