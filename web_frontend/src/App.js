// importing the required modules
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './App.css';

// declaring the variables
let option1 = [

];

let data_mapping = [];
// creating the App function
const SimpleLineChart = () => {
  const [dropdownValue, setDropdownValue] = useState('Option 1');
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [datas, setDatas] = useState([]);
  const [datat, setData] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => setDatas(data))
  }, []);

  // creating the handleDropdownChange function
  const handleDropdownChange = (event) => {
    // make the option1 empty
    option1 = [];
    setDropdownValue(event.target.value);
  };

  // creating the handleInputChange function
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  // creating the handleOptionClick function
  const handleOptionClick = (option) => {
    setSelectedOption(option.value);
    setInputValue(option.value);
    // setIsOpen(false);
  };

  const data_loader = (props) => {
    setData(props["mime"]);
    for (let i = 0; i < props["status"].length; i++) {
      data_mapping.push({ dataKey: props["status"][i], stroke: generateRandomColor() });
    }
  }

  // creating the handler function
  const handler = (props) => {
    // if (!props) return;
    const keys = Object.keys(props);
    const values = Object.values(props);
    for (let i = 0; i < keys.length; i++) {
      option1.push({ label: keys[i], value: values[i] });
    }
  }
  // console.log(option1)
  console.log(data_mapping)
  const clicker = () => {
    const body = {
      'name': dropdownValue,
      'text': inputValue
    }
    // fetching the data from the API
    fetch('http://127.0.0.1:8000/item', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
      .then(response => response.json())
      .then(data => data_loader(data));
  }

  // creating the generateRandomColor function which will generate random colors
  function generateRandomColor() {
    let maxVal = 0xFFFFFF;
    let randomNumber = Math.random() * maxVal;
    randomNumber = Math.floor(randomNumber);
    randomNumber = randomNumber.toString(16);
    let randColor = randomNumber.padStart(6, 0);
    return `#${randColor.toUpperCase()}`
  }

  // creating the handleCheckboxChange function
  const handleCheckboxChange = (e) => {
    option1 = [];
    setIsOpen(e.target.checked);
    const body = {
      'name': dropdownValue,
    }
    if (e.target.checked) {
      fetch('http://127.0.0.1:8000/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      })
        .then(response => response.json())
        .then(data => handler(data));
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ display: 'flex', flexGrow: 1 }}>
        <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <LineChart width={1200} height={800} data={datat} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <XAxis dataKey="name" />
            <YAxis label={{ value: 'log count', angle: -90, position: 'left' }} />
            <CartesianGrid stroke='#ccc' />
            <Tooltip />
            <Legend />
            {/* specifying the lines */}
            <Line type="monotone" dataKey="total_count" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="image/svg+xml" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="image/png" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="application/javascript" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="binary/octet-stream" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="text/javascript" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="text/css" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="text/html" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="text/plain" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="application/x-javascript" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="image/jpeg" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="application/json" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="200" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="204" stroke={generateRandomColor()} activeDot={{ r: 8 }} />
          </LineChart>
        </div>
        {/* adding the  querying elements*/}
        <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }} className="vision">
          <select value={dropdownValue} onChange={handleDropdownChange}>
            <option value="">Select an option</option>
            {Object.entries(datas).map(([key, value]) => (
              <option key={key} value={key + ':' + value.type}>{key + ' : ' + value.type}</option>
            ))}
          </select>
          <div>
            <input type="checkbox" id="vehicle1" name="vehicle1" value="Bike" onChange={handleCheckboxChange} />
            <label for="vehicle1">show fields</label><br />
          </div>
          <div>
            <div>
              <input type="text" value={inputValue} onChange={handleInputChange} className="rand" placeholder='enter the keyword' />
              {/* create a submit button */}
              <button type="submit" className="btn btn-primary" onClick={clicker}>Submit</button>
            </div>
            {isOpen && (
              <div style={{ maxHeight: '100px', overflowY: 'scroll', paddingRight: '20px' }}>
                {option1.map((option) => (
                  <div
                    key={option.value}
                    onClick={() => handleOptionClick(option)}
                    style={{ cursor: 'pointer' }}
                  >
                    {option.value}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// exporting the component
export default SimpleLineChart;