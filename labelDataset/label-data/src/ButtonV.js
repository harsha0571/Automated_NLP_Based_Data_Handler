import React from 'react'
import { useState, useEffect, useRef } from 'react'


const ButtonV = ({ word, keys, fn }) => {

    const [color, setColor] = useState("green")
    const firstUpdate = useRef(true)



    useEffect(() => {

        if (firstUpdate.current) {
            firstUpdate.current = false;
            return;
        }

        if (color === "red") {
            console.log(keys)
            const data = [...keys]
            if (!data.includes(word)) {
                data.push(word)
            }
            console.log(data)
            fn(data)
        } else if (color === "green") {

            // const myArray = [1, 2, 3, 4, 5];
            // const index = myArray.indexOf(2);
            // const x = myArray.splice(index, 1);

            const data = [...keys]
            if (data.includes(word)) {
                const index = data.indexOf(word)
                const x = data.splice(index, 1)
                fn(data)
            }

        }

    }, [color])

    function handleClick(e) {
        e.preventDefault()
        color === "red" ? setColor("green") : setColor("red")
    }

    return (
        <div>

            <button style={{ backgroundColor: `${color}` }} onClick={handleClick}>{word}</button>


        </div>
    )
}

export default ButtonV