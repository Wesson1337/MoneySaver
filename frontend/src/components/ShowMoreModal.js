import React, {useEffect, useState} from 'react';
import dots from "../static/icons/menu-dots-vertical.svg";
import {OPERATIONS_ROUTE} from "../utils/consts";

const ShowMoreModal = (props) => {
    const [isClicked, setIsClicked] = useState(false)

    return (
        <>
            <div
                onMouseEnter={() => props.setNavigateTo(null)}
                onMouseDown={() => setIsClicked(true)}
                onMouseUp={() => setIsClicked(false)}
                onMouseLeave={!props.showModal ? () => props.setNavigateTo(OPERATIONS_ROUTE): null}
                onClick={(e) => {
                    e.stopPropagation()
                    props.setNavigateTo(null)
                    props.setShowModal(true)
                }}
                className="d-flex justify-content-center align-items-center"
                style={{
                    width: "25px",
                    height: "25px",
                    cursor: "pointer",
                    filter: (props.navigateTo ? "" : "drop-shadow(2px 2px 3px rgba(2, 2, 2, 0.4))")
                    + ((props.showModal || isClicked) && !props.navigateTo ? "brightness(0.95)" : ""),
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