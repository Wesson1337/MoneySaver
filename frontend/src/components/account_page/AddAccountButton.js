import React, {useState} from 'react';
import {INTERFACE_COLORS} from "../../utils/consts";
import whitePlusIcon from "../../static/icons/plus-add-create-new-cross-svgrepo-com.svg";
import {Modal} from "react-bootstrap";

const AddAccountButton = () => {
    const [showAddModal, setShowAddModal] = useState(false)
    const handleOnHide = () => {
        setShowAddModal(false)
    }
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
            >

            </Modal>
        </>
    );
};

export default AddAccountButton;