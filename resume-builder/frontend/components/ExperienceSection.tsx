'use client';

import { UseFormReturn, FieldArrayWithId } from 'react-hook-form';
import { ResumeRequest, ExperienceItem } from '@/types/resume';

interface ExperienceSectionProps {
  form: UseFormReturn<ResumeRequest>;
  fields: (FieldArrayWithId<ResumeRequest, 'experience', 'id'> &
    ExperienceItem)[];
  onAdd: () => void;
  onRemove: (index: number) => void;
}

export default function ExperienceSection({
  form,
  fields,
  onAdd,
  onRemove,
}: ExperienceSectionProps) {
  const { register, formState } = form;
  const { errors } = formState;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Work Experience
        </h3>
        <button
          type="button"
          onClick={onAdd}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
        >
          + Add Experience
        </button>
      </div>

      {fields.length === 0 && (
        <div className="rounded-lg border-2 border-dashed border-gray-300 p-8 text-center">
          <p className="text-gray-500">No experience added yet</p>
          <button
            type="button"
            onClick={onAdd}
            className="mt-2 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            Add your first experience
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
              Experience #{index + 1}
            </span>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Company
              </label>
              <input
                {...register(`experience.${index}.company` as const, {
                  required: 'Company is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., Google"
              />
              {errors.experience?.[index]?.company && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.experience[index]?.company?.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Role
              </label>
              <input
                {...register(`experience.${index}.role` as const, {
                  required: 'Role is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., Software Engineer"
              />
              {errors.experience?.[index]?.role && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.experience[index]?.role?.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Start Date
              </label>
              <input
                {...register(`experience.${index}.start_date` as const, {
                  required: 'Start date is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., Jan 2020"
              />
              {errors.experience?.[index]?.start_date && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.experience[index]?.start_date?.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                End Date
              </label>
              <input
                {...register(`experience.${index}.end_date` as const, {
                  required: 'End date is required',
                })}
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                placeholder="e.g., Present"
              />
              {errors.experience?.[index]?.end_date && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.experience[index]?.end_date?.message}
                </p>
              )}
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700">
              Responsibilities & Achievements
            </label>
            <textarea
              {...register(`experience.${index}.responsibilities` as const, {
                required: 'Responsibilities are required',
              })}
              rows={4}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Describe your key responsibilities and achievements..."
            />
            {errors.experience?.[index]?.responsibilities && (
              <p className="mt-1 text-xs text-red-500">
                {errors.experience[index]?.responsibilities?.message}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
