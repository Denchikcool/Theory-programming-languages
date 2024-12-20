﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace lab4
{
    public class DPDA
    {
        private readonly List<string> _states;
        private readonly List<string> _inputAlphabet;
        private readonly List<string> _stackAlphabet;
        private readonly List<string> _inTransform;
        private readonly Dictionary<string, List<string>> _transitions;
        private readonly string _initialState;
        private readonly string _initialStackSymbol;
        private readonly List<string> _acceptingStates;

        private string _currentState;
        private Stack<string> _stack;
        public List<string> History { get; }
        public string OutputString { get; private set; }

        public DPDA() { }
        public DPDA(
            List<string> states,
            List<string> inputAlphabet,
            List<string> stackAlphabet,
            List<string> inTransform,
            Dictionary<string, List<string>> transitions,
            string initialState,
            string initialStackSymbol,
            List<string> acceptingStates)
        {
            _states = states;
            _inputAlphabet = inputAlphabet;
            _stackAlphabet = stackAlphabet;
            _inTransform = inTransform;
            _transitions = transitions;
            _initialState = initialState;
            _initialStackSymbol = initialStackSymbol;
            _acceptingStates = acceptingStates;

            History = new List<string>();
            OutputString = "";
        }

        public (bool Success, string Reason) Accept(string inputString)
        {
            Reset();

            foreach (char symbol in inputString)
            {
                var character = Step(symbol.ToString());
                if (!character.Success)
                {
                    return character;
                }
            }

            var stepResult = Step("");
            if (!stepResult.Success)
            {
                return stepResult;
            }
            if (_acceptingStates.Contains(_currentState))
            {
                return (true, "");
            }
            return (false, "Цепочка не завершилась в принимающем состоянии");
        }

        public void Reset()
        {
            _currentState = _initialState;
            _stack = new Stack<string>();
            _stack.Push(_initialStackSymbol);
            History.Clear();
            OutputString = "";
            History.Add($"Начальное состояние: {_currentState}, стек: {_initialStackSymbol}");
        }

        private (bool Success, string Reason) Step(string symbol)
        {
            if (!_inputAlphabet.Contains(symbol) && symbol != "")
            {
                return (false, $"В цепочке присутствуют посторонние символы (символа \"{symbol}\" нет в алфавите)!");
            }

            var stackTop = _stack.Count > 0 ? _stack.Peek() : null;
            var transitionKey = $"({_currentState}, {symbol}, {stackTop})";

            if (!_transitions.ContainsKey(transitionKey))
            {
                return (false, $"Нет перехода для ({_currentState}, {symbol}, {stackTop})");
            }

            var transition = _transitions[transitionKey];
            var nextState = transition[0];
            var newStackSymbols = transition[1];
            string outputSymbol;

            try
            {
                outputSymbol = transition[2];
            }
            catch (IndexOutOfRangeException)
            {
                return (false, "Не хватает выходного символа в переходе");
            }

            foreach (char c in outputSymbol)
            {
                if (!_inTransform.Contains(c.ToString()))
                {
                    return (false, $"Посторонний символ '{c}' в выходной цепочке!");
                }
            }

            _currentState = nextState;
            if (_stack.Count > 0)
            {
                _stack.Pop();
            }

            foreach (var newStackSymbol in newStackSymbols.Reverse())
            {
                _stack.Push(newStackSymbol.ToString());
            }
            OutputString += outputSymbol;

            History.Add($"Текущее состояние: {_currentState}, символ: {symbol}, стек: {string.Join(", ", _stack.ToArray())}, выход: {OutputString}");
            return (true, "");
        }
    }
}
