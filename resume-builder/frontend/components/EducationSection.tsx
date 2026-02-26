'use client';

import { UseFormReturn, FieldArrayWithId } from 'react-hook-form';
import { ResumeRequest, EducationItem } from '@/types/resume';

interface EducationSectionProps {
  form: UseFormReturn<ResumeRequest>;
  fields: (FieldArrayWithId<ResumeRequest, 'education', 'id'> &
    EducationItem)[];
  onAdd: () => void;
  onRemove: (index: number) => void;
}

export default function EducationSection({
  form,
  fields,
  onAdd,
  onRemove,
}: EducationSectionProps) {
  const { register, formState } = form;
  const { errors } = formState;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Education</h3>
        <button
          type="button"
          onClick={onAdd}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
        >
          + Add Education
        </button>
      </div>

      {fields.length === 0 && (
        <div className="rounded-lg border-2 border-dashed border-gray-300 p-8 text-center">
          <p className="text-gray-500">No education added yet</p>
          <button
            type="button"
            onClick={onAdd}
            className="mt-2 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            Add your first education
          </button>
        </div>
      )}

      {fields.map((field, index) => (
        <div
          key={field.id}
          className="relative rounded-lg border border-gray-200 bg-gray-50 p-6"
        >
          <button
            type="button"
            onClick={() => onRemove(index)}
            className="absolute right-4 top-4 text-gray-400 hover:text-red-500"
          >
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>

          <div className="mb-4">
            <span className="text-sm font-medium text-gray-500">
              Education #{index + 1}
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700">
                Degree
              </label>
              <input
                {...register(`education.${index}.degree` as const, {
                  required: 'Degree is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., Bachelor of Science in Computer Science"
              />
              {errors.education?.[index]?.degree && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.education[index]?.degree?.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Year
              </label>
              <input
                {...register(`education.${index}.year` as const, {
                  required: 'Year is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., 2020"
              />
              {errors.education?.[index]?.year && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.education[index]?.year?.message}
                </p>
              )}
            </div>

            <div className="sm:col-span-3">
              <label className="block text-sm font-medium text-gray-700">
                Institution
              </label>
              <input
                {...register(`education.${index}.institution` as const, {
                  required: 'Institution is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., Stanford University"
              />
              {errors.education?.[index]?.institution && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.education[index]?.institution?.message}
                </p>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
