import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import { getQuestionnaires, submitQuestionnaireAnswer } from '../services/api';
import { Questionnaire, Answer } from '../types/api'; // Assuming these types exist

interface AnswerState {
  [questionId: string]: any; // Value can be string, number, or array
}

const QuestionnairePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { token, user } = useContext(AuthContext);
  const [questionnaire, setQuestionnaire] = useState<Questionnaire | null>(null);
  const [answers, setAnswers] = useState<AnswerState>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuestionnaire = async () => {
      if (!token || !id) return;
      try {
        setLoading(true);
        const allQuestionnaires = await getQuestionnaires(token);
        const foundQuestionnaire = allQuestionnaires.find((q) => q.id === parseInt(id));
        if (foundQuestionnaire) {
          setQuestionnaire(foundQuestionnaire);
          // Initialize answers state with empty values based on question type
          const initialAnswers: AnswerState = {};
          foundQuestionnaire.questions.forEach(q => {
            if (q.type === 'number') initialAnswers[q.id] = '';
            else if (q.type === 'choice' && q.options && q.options.length > 0) initialAnswers[q.id] = ''; // Or first option
            else initialAnswers[q.id] = '';
          });
          setAnswers(initialAnswers);

        } else {
          setError('Questionnaire not found.');
        }
      } catch (err) {
        console.error('Error fetching questionnaire:', err);
        setError('Failed to load questionnaire.');
      } finally {
        setLoading(false);
      }
    };
    fetchQuestionnaire();
  }, [id, token]);

  const handleAnswerChange = (questionId: string, value: any) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !user || !questionnaire) return;

    // Convert answers state to the required API format
    const formattedAnswers: Answer[] = questionnaire.questions.map(q => ({
      question_id: q.id,
      value: answers[q.id]
    }));

    // Basic validation (can be more robust)
    const allAnswered = formattedAnswers.every(a => a.value !== undefined && a.value !== null && a.value !== '');
    if (!allAnswered) {
      alert("Please answer all questions before submitting.");
      return;
    }

    setSubmitting(true);
    try {
      await submitQuestionnaireAnswer(token, questionnaire.id, formattedAnswers);
      alert('Questionnaire submitted successfully!');
      navigate('/'); // Go back to home page
    } catch (err) {
      console.error('Error submitting answers:', err);
      setError('Failed to submit questionnaire. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="text-center p-8 text-gray-600">Loading questionnaire...</div>;
  }

  if (error) {
    return <div className="text-center p-8 text-red-600">{error}</div>;
  }

  if (!questionnaire) {
    return <div className="text-center p-8 text-gray-600">No questionnaire data available.</div>;
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">{questionnaire.title}</h2>
      {questionnaire.description && (
        <p className="text-gray-600 mb-6">{questionnaire.description}</p>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {questionnaire.questions.map((q) => (
          <div key={q.id} className="border border-gray-200 p-5 rounded-lg bg-gray-50">
            <label htmlFor={q.id} className="block text-lg font-medium text-gray-700 mb-2">
              {q.text}
            </label>
            {q.type === 'text' && (
              <input
                type="text"
                id={q.id}
                value={answers[q.id] || ''}
                onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                className="mt-1 block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                required
              />
            )}
            {q.type === 'number' && (
              <input
                type="number"
                id={q.id}
                value={answers[q.id] || ''}
                onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                className="mt-1 block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                required
              />
            )}
            {q.type === 'choice' && q.options && (
              <select
                id={q.id}
                value={answers[q.id] || ''}
                onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                className="mt-1 block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-white"
                required
              >
                <option value="">Select an option</option>
                {q.options.map((option) => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
            )}
          </div>
        ))}

        <div className="flex justify-end space-x-4 mt-6">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-6 py-3 border border-gray-300 rounded-md shadow-sm text-lg font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="px-6 py-3 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? 'Submitting...' : 'Submit Answers'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default QuestionnairePage;