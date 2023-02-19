import React from 'react'
import { useState, useEffect, useRef } from 'react'


const ButtonS = ({ word, cur, fn }) => {

    const [title, setTitle] = useState(word)
    const [color, setColor] = useState("green")
    const [valid, setValid] = useState("valid")
    const [backup, setBackup] = useState("")
    const [idx, setIdx] = useState()

    useEffect(() => {
        const data = [...cur];

        var index = data.indexOf(word);
        data[index] = title;
        fn(data)
    }, [title])
    const firstUpdate = useRef(true);
    useEffect(() => {

        if (firstUpdate.current) {
            firstUpdate.current = false;
            return;
        }

        if (backup) {
            const data = [...cur];
            data[idx] = backup
            fn(data)
            setBackup("")
        }
        else {
            const data = [...cur];
            var index = data.indexOf(word);
            setIdx(index)
            setBackup(title)
            data[index] = "";
            fn(data)

        }

    }, [valid])

    const handleChange = (event) => {
        setTitle(event.target.value)
    };

    function handleClick(e) {
        color === "red" ? setColor("green") : setColor("red")
        valid === "valid" ? setValid("remove") : setValid("valid")
    }

    // const updatedStudentData = [...studentData];
    // updatedStudentData.push(data);
    // setStudentData(updatedStudentData);

    return (
        <div>

            <input type='text' value={title} onChange={(e) => { handleChange(e) }} />

            <button style={{ backgroundColor: `${color}` }} onClick={handleClick}>{valid}</button>
            {/* <button style={{ color: "red", marginTop: "40px" }}>
                {title}
            </button> */}
        </div>
    )
}

export default ButtonS