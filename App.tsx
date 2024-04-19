import react, { useState, useEffect } from 'react'
import axios from 'axios';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, BarChart, Bar } from 'recharts';




import './App.css'
import ProductTable from './ProductTable';



function App() {
  const [data, setData] = useState({})
  const [display, setDisplay] = useState()
  const [showTable, setShowTable] = useState(false);
  const [showTable1, setShowTable1] = useState(false);
  const [showGraph, setShowGraph] = useState(false);
  const [showGraph1, setShowGraph1] = useState(false);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const [graph, setGraph] = useState();



  function handleClick() {
    console.log('a', data.name);
    const parameter = {
      key1: `C:\\Users\\admin\\Desktop\\finalpdf\\${data.name}`,
      param1: startDate,
      param2: endDate
    };
    axios.post('http://localhost:5000/api/data', parameter
    )
      .then(response => {
        // Handle the successful response
        console.log("Data from API:", response.data);
        setDisplay(prev => response.data);
        setShowTable1(false)
        setShowTable(true)
        setShowGraph(false)
      })
  };

  function showdata(event) {
    console.log(event);

    switch(event) {
      case "item1":

      const sortedData = display.main.sort((a, b) => {
        return parseInt(a.Qty) - parseInt(b.Qty);
    });
      const filteredData = sortedData.map(item => {
        return {
            "Article Description": item["Article Description"],
            "Qty": item["Qty"]
        };
    })
    const top10Objects = filteredData.slice(-10);
    
    setGraph(top10Objects)
      setShowGraph(true)
  

        
        break;

      case "item2":
        const sortedData1 = display.main.sort((a, b) => {
          return parseInt(a.Qty) - parseInt(b.Qty);
      });
        const filteredData1 = sortedData1.map(item => {
          return {
              "Article Description": item["Article Description"],
              "Qty": item["Qty"]
          };
      })
      const top10Objects1 = filteredData1.slice(0, 10);
      
        setGraph(top10Objects1)
        setShowGraph(true)
    
       
        break;
 
      // Add more cases as needed
      default:
        const itemsArray = Object.keys(display.main['Article Description']).map(key => ({
          description: display.main['Article Description'][key],
          quantity: display.main['Qty'][key]
        }));
        setGraph(itemsArray)
        setShowGraph(true)
        break;
    }

    
//     try{
//     console.log(display.main['Article Description']);
//     const itemsArray = Object.keys(display.main['Article Description']).map(key => ({
//       description: display.main['Article Description'][key],
//       quantity: display.main['Qty'][key]
//     }));
//     setGraph(itemsArray)
//     setShowGraph(true)
//   }catch(error){
//     const sortedData = display.main.sort((a, b) => {
//       return parseInt(a.Qty) - parseInt(b.Qty);
//   });
//     const filteredData = sortedData.map(item => {
//       return {
//           "Article Description": item["Article Description"],
//           "Qty": item["Qty"]
//       };
//   })
//   const top10Objects = filteredData.slice(0, 10);
  
//   setGraph(top10Objects)
//     setShowGraph(true)
// }
    

  }
  function GetMonths() {
    // console.log(Object.keys(display.main[0]));
    const parameter = {
      key1: `C:\\Users\\admin\\Desktop\\finalpdf\\${data.name}`,
      param1: startDate,
      param2: endDate
    };
    
    axios.post('http://localhost:5000/api/WholeData', parameter
    )
      .then(response => {
        // Handle the successful response
        console.log("Data from API:", response.data);
        // console.log(response);
        if (response.data.main.length <1){
          alert("There no data found for the date between " + startDate + " and " + endDate);
          return
        }
        
        setDisplay(response.data);
        setShowTable(false)
        setShowTable1(true)
        setShowGraph(false)
      })
    // console.log(Object.keys(display.main[0]));
  }

  function ShowSinglePdfBar() {
    const itemsArray = Object.keys(display.main['Article Description']).map(key => ({
      description: display.main['Article Description'][key],
      quantity: display.main['Qty'][key]
    }));
    setGraph1(itemsArray)
    setShowGraph1(true)
    


  }

  return (
    <>
<nav className="navbar">
  <div className="logo">Himalaya Sell Analysis</div>
  <input type="file" id="file-upload" style={{ display: 'none' }} onChange={(e) => setData(e.target.files[0])} />
  <label htmlFor="file-upload" className="upload-button">Choose File</label>
  <button className="upload-button" onClick={handleClick}>Upload</button>

  <div className="date-selector">
   
    <div>
      <label htmlFor="start-date">Start Date:</label>
      <input
        type="date"
        id="start-date"
        onChange={(e) => setStartDate(e.target.value)}
      />
    </div>
    <div>
      <label htmlFor="end-date">End Date:</label>
      <input
        type="date"
        id="end-date"
        onChange={(e) => setEndDate(e.target.value)}
      />
      <button onClick={GetMonths}>Show </button>
    </div>
  </div>
</nav>





      {showTable &&
        <>

          <table className="fade-in">
            <tbody>
              {Object.keys(display.df).map(key => (
                <tr key={key}> {/* Added key prop for React list rendering */}
                  <th>{key}</th>
                  <td>{display.df[key]}</td> {/* Use square brackets to access property dynamically */}
                </tr>
              ))}

              {Object.keys(display.data).map(key => (
                <tr key={key}> {/* Added key prop for React list rendering */}
                  <th>{key}</th>
                  <td>{display.data[key]}</td> {/* Use square brackets to access property dynamically */}
                </tr>
              ))}
            </tbody>

          </table>

          <table className="fade-in">
            <thead>
              <tr>
                {/* Render table headers */}
                {Object.keys(display.main).map(key => (
                  <th>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {/* Render table rows */}
              {
                Object.values(display.main['Article Description']).map((value, index) => (
                  <tr>

                    {Object.keys(display.main).map((key, i) => (
                      <td>{display.main[key][index]}</td>
                    ))}
                  </tr>
                ))
              }
            </tbody>
          </table>
          <button className="custom-button" onClick={ShowSinglePdfBar}>Plot Bar Data</button>

          
          </>
      }

      {showTable1 &&
        <>

          <table>
            <thead>
              <tr>
                {Object.keys(display.main[0]).map((key, index) => (
                  <th key={index}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
        {display.main.map((row, index) => ( 
          <tr key={index}>
            {Object.values(row).map((value, index) => (
              <td key={index}>{value}</td>
            ))}
          </tr>
        ))}
      </tbody>
          </table>

          <div className="animated-div">

{/* <button onClick={showdata}>Show Graph</button> */}

<select value='' onChange={(e)=>showdata(e.target.value)}>
<option value="">Select an item</option>
<option value="item1">Highest Selling items</option>
<option value="item2">Lowest Selling Items</option>

</select>


</div>
        </>


      }


     

      {showGraph && <>
        <h1 className="chart-heading">Bar Chart of  Selling items between {startDate} and {endDate}</h1>
        <ResponsiveContainer width="100%" aspect={3}>
          <BarChart
            width={500}
            height={300}
            data={graph}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="Article Description"
              label={{ angle:60, position: 'bottom', fontSize: 12 }} />
            {/* Rotate by -90 degrees */}
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Qty" fill="#88318d8" />
          </BarChart>
        </ResponsiveContainer>



      </>

      }
{showGraph1 && <>
        <h1 className="chart-heading">Bar Chart of  Selling items between {startDate} and {endDate}</h1>
        <ResponsiveContainer width="100%" aspect={3}>
          <BarChart
            width={500}
            height={300}
            data={graph}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="Article Description"
              label={{ angle:60, position: 'bottom', fontSize: 12 }} />
            {/* Rotate by -90 degrees */}
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Qty" fill="#88318d8" />
          </BarChart>
        </ResponsiveContainer>



      </>

      }

    </>



    
  )
}

export default App
