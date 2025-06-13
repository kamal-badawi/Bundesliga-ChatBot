import React, { useState, useEffect } from 'react';
import axios from 'axios';

import TopSection from './TopSection';
import MiddleSection from './MiddleSection';
import BottomSection from './BottomSection';
import MenuSection from './MenuSection';

const todayFormatted = new Date().toLocaleDateString('de-DE', {
  day: 'numeric',
  month: 'long',
  year: 'numeric',
});

const AppController = () => {
  const userId = "user_001";

  const [conversationId, setConversationId] = useState("");
  const [isAppLoading, setIsAppLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [showMenuSection, setShowMenuSection] = useState(false);
  const [isMenuOpening, setIsMenuOpening] = useState(false);
  const [fetchTitles, setFetchTitles] = useState(false);
  const [conversationsTitles, setConversationsTitles] = useState<any[]>([]);
  const [filteredConversationsTitles, setFilteredConversationsTitles] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  

  console.log('question:',question);
  console.log('answer: ',answer)
  const fetchAnswer = async () => {
    try {
      const response = await axios.post('http://localhost:8000/question', {
      question: question,
    });
    console.log('response:',response)

      const answer = response.data.answer;

      setAnswer(answer);
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        console.error('Keine Antwort gefunden.');
      } else {
        console.error('Fehler beim Abrufen der Antwort:', error.message);
      }
    }
  };

   useEffect(() => {
    fetchAnswer();
  }, [question]);

  


  const fetchConversationTitles = async () => {
    try {
      const response = await axios.post('http://localhost:8000/conversations_titles', {
        user_id: userId,
      });

      const titles = response.data.conversations_titles;
      const ids = response.data.conversations_ids;

      const mergedConversations = titles.map((title: string, index: number) => ({
        conversation_id: ids[index],
        title: title,
      }));

      setConversationsTitles(mergedConversations);
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        console.error('Keine Gesprächstitel gefunden.');
      } else {
        console.error('Fehler beim Abrufen der Gesprächstitel:', error.message);
      }
    }
  };

  useEffect(() => {
    if (fetchTitles === true) {
      fetchConversationTitles();
    } else {
      setConversationsTitles([]);
    }
  }, [fetchTitles]);

  useEffect(() => {
    setFilteredConversationsTitles(
      conversationsTitles.filter((conv) =>
        conv.title.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm, conversationsTitles]);

 

  return (
  <div className="flex h-screen">
    {/* Sidebar */}
    <div
      className={`transition-all duration-300 ${
        isMenuOpening ? 'w-1/4 p-4' : 'w-0 p-0'
      } bg-yellow-50 border-r-2 border-black overflow-y-auto`}
    >
      {isMenuOpening && (
        <MenuSection
          userId={userId}
          conversationsTitles={filteredConversationsTitles}
          setConversationsTitles={setConversationsTitles}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          setConversationId={setConversationId}
        />
      )}
    </div>

    {/* Main Area */}
    <div className="flex-1 flex flex-col overflow-hidden relative">
      {/* Top Header */}
      <div className="w-full bg-yellow-50 border-b-2 border-black">
        <TopSection
          setMessages={setMessages}
          date={todayFormatted}
          isMenuOpening={isMenuOpening}
          setIsMenuOpening={setIsMenuOpening}
          setShowMenuSection={setShowMenuSection}
          setFetchTitles={setFetchTitles}
        />
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto">
        <MiddleSection userId={userId} conversationId={conversationId} />
        <BottomSection question={question} setQuestion={setQuestion} isMenuOpening={isMenuOpening} />
      </div>

     
    </div>
  </div>
);

};

export default AppController;
