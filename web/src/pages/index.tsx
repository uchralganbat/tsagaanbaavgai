import Image from 'next/image'
import { Inter } from 'next/font/google'
import { useState } from 'react'
import axios from 'axios'

const inter = Inter({ subsets: ['latin'] })


export default function Home() {
  
  const [prompt, setPrompt] = useState('')
  const onSubmit = (prompt: String) => {
    console.log(prompt + ' was submitted')
    if(prompt.length > 0) {
      axios.get('localhost:4000')
    }
  }
  const onChange = (event: any) => {
    setPrompt(event.target.value)
  }
  return (
    <main className="container">
      <h1>Twitter</h1>
      <div className="">
        <input
          placeholder='keyword' 
          onChange={onChange} 
          onKeyDown={(event: any) => {
            if(event.keyCode == 13){
              onSubmit(prompt)
              event.target.value = ''
            }
          }}
        />
      </div>
    </main>
  )
}
