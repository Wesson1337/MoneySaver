import React, {useState} from 'react';
import {Card} from "react-bootstrap";
import {useNavigate} from "react-router-dom";

const MainPageCard = ({className, showModal, style, id, navigateto, children}) => {
    const [isActive, setIsActive] = useState(false)
    const [isClicked, setIsClicked] = useState(false)
    const navigate = useNavigate()
    return (
        <Card
            className={"p-3 " + className}
            onMouseDown={!showModal ? () => setIsClicked(true) : null}
            onMouseUp={() => {
                setIsActive(false);
                setIsClicked(false)
            }}
            onMouseEnter={() => {
                setIsClicked(false);
                setIsActive(true)
            }}
            onMouseLeave={() => {
                setIsClicked(false);
                setIsActive(false)
            }}
            onClick={!showModal ? () => {
                navigate(navigateto)
            } : null}
            style={Object.assign({
                filter: (isActive && navigateto ? "drop-shadow(2px 2px 2px rgba(2, 2, 2, 0.2))" : "")
                    + (isClicked && navigateto ? "brightness(0.95)" : ""),
                transition: "0.25s ease-out",
                cursor: "pointer"
            }, style)}
            id={id}
        >
            {children}
        </Card>
    );
};

export default MainPageCard;