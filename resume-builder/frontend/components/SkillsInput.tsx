'use client';

import { useState, KeyboardEvent } from 'react';

interface SkillsInputProps {
  skills: string[];
  onChange: (skills: string[]) => void;
}

export default function SkillsInput({ skills, onChange }: SkillsInputProps) {
  const [inputValue, setInputValue] = useState('');

  const addSkill = (skill: string) => {
    const trimmedSkill = skill.trim();
    if (trimmedSkill && !skills.includes(trimmedSkill)) {
      onChange([...skills, trimmedSkill]);
      setInputValue('');
    }
  };

  const removeSkill = (skillToRemove: string) => {
    onChange(skills.filter((skill) => skill !== skillToRemove));
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addSkill(inputValue);
    } else if (e.key === 'Backspace' && inputValue === '' && skills.length > 0) {
      removeSkill(skills[skills.length - 1]);
    }
  };

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Skills (Press Enter or comma to add)
      </label>
      <div className="min-h-[42px] rounded-lg border border-gray-300 bg-white p-2 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-200">
        <div className="flex flex-wrap gap-2">
          {skills.map((skill) => (
            <span
              key={skill}
              className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-700"
            >
              {skill}
              <button
                type="button"
                onClick={() => removeSkill(skill)}
                className="rounded-full p-0.5 hover:bg-blue-200"
              >
                <svg
                  className="h-3 w-3"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </span>
          ))}
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 min-w-[120px] border-none outline-none text-gray-700"
            placeholder={skills.length === 0 ? 'Add skills...' : ''}
          />
        </div>
      </div>
      {skills.length > 0 && (
        <p className="text-xs text-gray-500">{skills.length} skill(s) added</p>
      )}
    </div>
  );
}
