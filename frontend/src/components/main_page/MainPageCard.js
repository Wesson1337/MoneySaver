import React, {useState} from 'react';
import {Card} from "react-bootstrap";
import {useNavigate} from "react-router-dom";

const MainPageCard = (props) => {
    const [isActive, setIsActive] = useState(false)
    const navigate = useNavigate()
    return (
        <Card
            className="w-25 p-3"
            onMouseEnter={() => setIsActive(true)}
            onMouseLeave={() => setIsActive(false)}
            onClick={() => navigate(props.navigateTo)}
            style={{
                filter: isActive ? "drop-shadow(1px 1px 2px rgba(2, 2, 2, 0.14))" : null,
                transition: "0.25s",
                cursor: "pointer"
            }}
        >
            {props.children}
        </Card>
    );
};

export default MainPageCard;