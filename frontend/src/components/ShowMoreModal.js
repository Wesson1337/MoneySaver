import React, {useEffect, useState} from 'react';
import dots from "../static/icons/menu-dots-vertical.svg";
import {OPERATIONS_ROUTE} from "../utils/consts";

const ShowMoreModal = (props) => {
    const [isClicked, setIsClicked] = useState(false)
    const [isActive, setIsActive] = useState(false)

    return (
        <>
            <div
                onMouseDown={(e) => {e.stopPropagation(); setIsClicked(true)}}
                onMouseUp={(e) => {e.stopPropagation(); setIsClicked(false)}}
                onMouseEnter={() => setIsActive(true)}
                onMouseLeave={() => setIsActive(false)}
                onClick={(e) => {
                    e.stopPropagation()
                    props.setShowModal(true)
                }}
                className="d-flex justify-content-center align-items-center"
                style={{
                    width: "25px",
                    height: "25px",
                    cursor: "pointer",
                    filter: (isActive || props.showModal ? "drop-shadow(2px 2px 3px rgba(2, 2, 2, 0.4))" : "")
                    + (props.showModal || isClicked ? "brightness(0.95)" : ""),
                    transition: "0.25s",
                    background: "white",
                    borderRadius: "3px"
                }}>
                <img src={dots} alt={""} height={15}/>
            </div>
            {props.children}
        </>
    );
};

export default ShowMoreModal;