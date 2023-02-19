
import './App.css';
import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import ButtonS from './ButtonS';
import ButtonV from './ButtonV';

function App() {
  const [id, setId] = useState()
  const [curTitle, setCurTitle] = useState([])
  const [flag, setFlag] = useState(false)
  const [vertitle, setVerTitle] = useState([])
  const [keywords, setKeywords] = useState([])

  useEffect(() => {
    async function getData() {
      let resp = await axios.get("http://localhost:5000/id/latest")
      setId(resp.data.data)

      let curtitle = await axios.get(`http://localhost:5000/file/${resp.data.data}`)

      setCurTitle(curtitle.data.data.split(" "))

    }
    getData()
  }, [])


  // window.location.reload();

  const firstUpdate = useRef(true)
  useEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
    let temp = []
    for (let i = 0; i < curTitle.length; i++) {
      let tmp = curTitle[i].split(" ")
      for (let j = 0; j < tmp.length; j++) {
        temp.push(tmp[j])
      }
    }


    setVerTitle(temp)
    // console.log(vertitle.join(" "))

  }, [curTitle])

  const listItems = curTitle.map((word) => {
    // <button style={{ color: "red", marginRight: "10px" }}>{word}</button>

    return <ButtonS word={word} cur={curTitle} fn={setCurTitle} />

  }
  );

  const listVerItems = vertitle.map((word) => {
    // <button style={{ color: "red", marginRight: "10px" }}>{word}</button>
    if (word !== "") {
      return <ButtonV word={word} keys={keywords} fn={setKeywords} />
    }
  }
  );

  function handleReload() {
    window.location.reload()
  }

  function handleSubmit() {
    let temp = []
    for (let i = 0; i < vertitle.length; i++) {
      if (keywords.includes(vertitle[i])) {
        temp.push(vertitle[i])
      }
    }

    let text1 = vertitle.join(" ")
    let text2 = text1.trimEnd()
    let text3 = text2.trimStart()

    const post = {
      title: text3,
      keywords: temp
    }

    // axios.post("https://tempusapi.herokuapp.com/db/watch_history", hist, {
    //                       headers: {
    //                           authorization: `bearer ${tk}`
    //                       }
    //                   }).then(res4 =>
    //                       console.log("sucess in history entry", res4))
    //                       .catch(error4 => console.log(error4))
    //               }

    axios.post("http://localhost:5000/file", post)
      .then(res => {
        console.log(res)
        axios.get("http://localhost:5000/id/update")
          .then(resp => { window.location.reload() })
          .catch(error => { console.log(error) })

      })
      .catch(err => { console.log(err) })

    //  window.location.reload()
  }


  return (
    <div className="App">
      <h1>Current Line : {id}</h1>


      <button onClick={(e) => { setFlag(!flag) }}>Verified Title</button>

      {flag ?
        <div>
          <p>Actual Title : {vertitle.join(" ")}</p>
          {listVerItems}
          <div>
            <button style={{ marginRight: "20px", marginTop: "20px" }} onClick={handleReload}>RESET</button>
            <button style={{ marginRight: "20px", marginTop: "20px" }} onClick={handleSubmit}> SUBMIT </button>
          </div>
        </div>
        :
        <div>
          {listItems}

        </div>
      }
    </div>
  );
}

export default App;
