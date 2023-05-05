import React, {useState} from 'react';
import {useLocation} from "react-router-dom";
import {INTERFACE_COLORS} from "../../utils/consts";
import whitePlusIcon from "../../static/icons/plus-add-create-new-cross-svgrepo-com.svg"
import whiteMinusIcon from "../../static/icons/minus-remove-subtract-delete-svgrepo-com.svg"
import AddTransactionModal from "./AddTransactionModal";

const AddTransactionButtons = ({data, hasChanged, setHasChanged}) => {
    const [showAddModal, setShowAddModal] = useState(false)
    const [showRemoveModal, setShowRemoveModal] = useState(false)
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
            <AddTransactionModal
                show={showAddModal}
                setShow={setShowAddModal}
                type="add"
                data={data}
                hasChanged={hasChanged}
                setHasChanged={setHasChanged}
            />
            <button
                style={{
                    width: "56px",
                    height: "56px",
                    border: "0px",
                    borderRadius: "50%",
                    background: INTERFACE_COLORS.RED
                }}
                className="d-flex align-items-center justify-content-center"
                onClick={() => {
                    setShowRemoveModal(true)
                }}
            >
                <img
                    src={whiteMinusIcon}
                    alt=""
                    width="23px"
                    color="white"
                />
            </button>
            <AddTransactionModal
                show={showRemoveModal}
                setShow={setShowRemoveModal}
                type="remove"
                data={data}
                hasChanged={hasChanged}
                setHasChanged={setHasChanged}
            />
        </div>
    );
};

export default AddTransactionButtons;