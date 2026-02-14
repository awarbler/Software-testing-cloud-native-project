
import {Button, TextField} from "@mui/material";
import { useState } from "react";
import "./HardwareSetRow.css";
type Props = {
    label: string;
    isJoined: boolean;
    onCheckIn?: (qty: number) => void;
    onCheckOut?: (qty: number) => void;
}

export default function HardwareSetRow({
    label,
    isJoined,
    onCheckIn,
    onCheckOut
}: Props){ // one hardware set row

    const [qty, setQty] = useState(""); // state for quantity input



    return (
        <div className="hw-row">
            <div className="hw-label">{label}</div>

            <TextField
                //label="Enter qty"
                size="small"
                placeholder="Enter qty"
                //value={qty}
                //onChange={handleQtyChange}
                className="hw-qty"
                disabled={!isJoined}
            />

            <Button
                className="hw-btn"
                variant="contained"
                //onClick={handleCheckInClick}
                disabled={!isJoined}
                >
                    Check In
            </Button>
            <Button
                className="hw-btn"
                variant="contained"
                //onClick={handleCheckOutClick}
                disabled={!isJoined}
                >
                    Check Out
            </Button>

        </div>
    );
}

