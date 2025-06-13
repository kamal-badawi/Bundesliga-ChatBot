import React, { useState } from 'react';
import axios from 'axios';







interface TopSectionProps {
  setMessages: React.Dispatch<React.SetStateAction<any[]>>;
  date: string;
  isMenuOpening: boolean;
  setIsMenuOpening: React.Dispatch<React.SetStateAction<boolean>>;
  setShowMenuSection: React.Dispatch<React.SetStateAction<boolean>>;
  setFetchTitles: React.Dispatch<React.SetStateAction<boolean>>;
 
 
}


const TopSection: React.FC<TopSectionProps> = ({ setMessages, date,isMenuOpening, setIsMenuOpening,setShowMenuSection,setFetchTitles}) => {
  
  const [isReseting, setIsReseting] = useState(false);

  const openCloseMenu = () => {
    if (isMenuOpening) {
      setIsMenuOpening(false);
      setShowMenuSection(false);
      setFetchTitles(false)
    } else {
      setIsMenuOpening(true);
      setShowMenuSection(true);
      setFetchTitles(true);
      
    }
   
  };
  
 
  const resetConversation = async ()=>{
    setIsReseting(true)
    try {
    const response = await axios.get('http://127.0.0.1:8000/reset_conversation');
    if (response.status ===200){
      setMessages([])
      console.log('Conversation has been reseted')
    }
    }

    catch (error){
      console.error('Fehler beim Zurücksetzen der Unterhaltung:', error);

    }
    finally{
      setIsReseting(false)
    }
    
  }

  return(

   
      
    
  <div
    className={' flex flex-row justify-between items-center bg-yellow-50 p-5 border-b-2 border-black'}
  >

    

      {/* Open & Close Menu Section Symbol */}
      <div className="flex items-start p-5">
  <button
    onClick={openCloseMenu}
    className="transition-transform duration-200 ease-in-out hover:scale-110 active:scale-95 text-gray-700 hover:text-blue-500"
  >
    {isMenuOpening ? (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={0.5}
        stroke="currentColor"
        className="size-12"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M3.75 6.75h16.5M3.75 12h16.5M12 17.25h8.25"
        />
      </svg>
    ) : (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={0.5}
        stroke="currentColor"
        className="size-12"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12"
        />
      </svg>
    )}
  </button>
</div>

       
    
    <div className="italic font-extrabold ">
      Logo
    </div>

    <div className="flex flex-col justify-between items-start">
    
    
    <div className="italic font-extrabold ">
    BundesLiga-ChatBot
    </div>
    <div >
   {date}
    </div>
    </div>
    
    
   
    <div >
    <button onClick={()=>{resetConversation()}} >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
</svg>


    </button>
  </div>
  </div>
  
  );

}
export default TopSection;
