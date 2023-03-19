import React, {useState} from 'react';
import {useLocation} from "react-router-dom";
import {INTERFACE_COLORS, OPERATIONS_ROUTE} from "../utils/consts";
import whitePlusIcon from "../static/icons/plus-add-create-new-cross-svgrepo-com.svg"
import whiteMinusIcon from "../static/icons/minus-remove-subtract-delete-svgrepo-com.svg"
import {Modal} from "react-bootstrap";

const AddRemoveButtons = (props) => {
    const location = useLocation()
    const isOperations = location.pathname === OPERATIONS_ROUTE
    const [greenIsActive, setGreenIsActive] = useState(false)
    const [greenIsClick, setGreenIsClicked] = useState(false)
    return (
        <div
            className="d-flex flex-column gap-4"
            style={{position: "fixed", bottom: "4%", right: "5%"}}
        >
            <button
                style={{width: "56px", height: "56px", border: "0px", borderRadius: "50%", background: INTERFACE_COLORS.GREEN}}
                className="d-flex align-items-center justify-content-center"
            >
                <img
                    src={whitePlusIcon}
                    alt=""
                    width="25px"
                />
                <>
                    {isOperations
                        ?
                        <Modal>

                        </Modal>
                        :
                        null
                    }
                </>
            </button>
            <button
                style={{width: "56px", height: "56px", border: "0px", borderRadius: "50%", background: INTERFACE_COLORS.RED}}
                className="d-flex align-items-center justify-content-center"
            >
                <img
                    src={whiteMinusIcon}
                    alt=""
                    width="23px"
                    color="white"
                />
            </button>
        </div>
    );
};

export default AddRemoveButtons;