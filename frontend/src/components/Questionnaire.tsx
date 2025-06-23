import React, { useState } from "react";

interface Question {
  id: number;
  question: string;
  options: string[];
}

interface QuestionnaireProps {
  questions: Question[];
  onSubmit?: () => void;
}

const Questionnaire: React.FC<QuestionnaireProps> = ({
  questions,
  onSubmit,
}) => {
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});

  const handleAnswerChange = (questionId: number, answer: string) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleSubmit = () => {
    // Here you would typically send the answers to the backend
    console.log("Submitted Answers:", answers);
    if (onSubmit) onSubmit();
  };

  return (
    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "16px",
        marginTop: "20px",
      }}
    >
      <h3>Questionnaire</h3>
      {questions.map((q) => (
        <div key={q.id} style={{ marginBottom: "16px" }}>
          <p>{q.question}</p>
          {q.options.map((option) => (
            <label key={option} style={{ marginRight: "16px" }}>
              <input
                type="radio"
                name={`question-${q.id}`}
                value={option}
                onChange={() => handleAnswerChange(q.id, option)}
              />
              {option}
            </label>
          ))}
        </div>
      ))}
      <button
        onClick={handleSubmit}
        style={{
          padding: "8px 16px",
          borderRadius: "4px",
          border: "none",
          background: "#28a745",
          color: "white",
          cursor: "pointer",
        }}
      >
        Submit Answers
      </button>
    </div>
  );
};

export default Questionnaire;
