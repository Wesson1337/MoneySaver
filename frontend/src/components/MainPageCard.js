import React, {useState} from 'react';
import {Card} from "react-bootstrap";
import {useNavigate} from "react-router-dom";

const MainPageCard = (props) => {
    const [isActive, setIsActive] = useState(false)
    const navigate = useNavigate()
    return (
        <Card
            className={"p-3 " + props.className}
            onMouseEnter={() => setIsActive(true)}
            onMouseLeave={() => setIsActive(false)}
            onClick={() => navigate(props.navigateto)}
            style={Object.assign({
                filter: isActive ? "drop-shadow(2px 2px 2px rgba(2, 2, 2, 0.2))" : null,
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