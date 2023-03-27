import React, {useState} from 'react';
import {useLocation} from "react-router-dom";
import {INTERFACE_COLORS, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE} from "../utils/consts";
import whitePlusIcon from "../static/icons/plus-add-create-new-cross-svgrepo-com.svg"
import whiteMinusIcon from "../static/icons/minus-remove-subtract-delete-svgrepo-com.svg"
import {Dropdown, DropdownButton, Modal} from "react-bootstrap";
import AddRemoveOperationModal from "./AddRemoveOperationModal";

const AddRemoveButtons = (props) => {
    const location = useLocation()
    const isOperations = location.pathname === OPERATIONS_ROUTE || location.pathname === MAIN_PAGE_ROUTE
    const [showAddModal, setShowAddModal] = useState(false)
    const [showRemoveModal, setShowRemoveModal] = useState(false)
    const [greenIsActive, setGreenIsActive] = useState(false)
    const [greenIsClick, setGreenIsClicked] = useState(false)
    return (
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
                    background: INTERFACE_COLORS.GREEN
                }}
                className="d-flex align-items-center justify-content-center"
                onClick={() => {setShowAddModal(true)}}
            >
                <img
                    src={whitePlusIcon}
                    alt=""
                    width="25px"
                />
            </button>
            {
                isOperations
                    ?
            <AddRemoveOperationModal
                show={showAddModal}
                setShow={setShowAddModal}
                type="add"
            />
                    :
                    null
            }
            <button
                style={{
                    width: "56px",
                    height: "56px",
                    border: "0px",
                    borderRadius: "50%",
                    background: INTERFACE_COLORS.RED
                }}
                className="d-flex align-items-center justify-content-center"
                onClick={() => {setShowRemoveModal(true)}}
            >
                <img
                    src={whiteMinusIcon}
                    alt=""
                    width="23px"
                    color="white"
                />
            </button>
            {
                isOperations
                    ?
                    <AddRemoveOperationModal
                        show={showRemoveModal}
                        setShow={setShowRemoveModal}
                        type="remove"
                    />
                    :
                    null
            }
        </div>
    );
};

export default AddRemoveButtons;