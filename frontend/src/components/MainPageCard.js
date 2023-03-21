import React, {useState} from 'react';
import {Card} from "react-bootstrap";
import {useNavigate} from "react-router-dom";

const MainPageCard = (props) => {
    const [isActive, setIsActive] = useState(false)
    const [isClicked, setIsClicked] = useState(false)
    const navigate = useNavigate()
    return (
        <Card
            className={"p-3 " + props.className}
            onMouseDown={!props.showModal ? () => setIsClicked(true) : null}
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
            onClick={!props.showModal ? () => {
                navigate(props.navigateto)
            } : null}
            style={Object.assign({
                filter: (isActive && props.navigateto ? "drop-shadow(2px 2px 2px rgba(2, 2, 2, 0.2))" : "")
                    + (isClicked && props.navigateto ? "brightness(0.95)" : ""),
                transition: "0.25s",
                cursor: "pointer"
            }, props.style)}
            id={props.id}
        >
            {props.children}
        </Card>
    );
};

export default MainPageCard;