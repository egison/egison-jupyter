import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IEditorLanguageRegistry } from '@jupyterlab/codemirror';
import {
  StreamLanguage,
  StreamParser,
  StringStream,
  LanguageSupport
} from '@codemirror/language';

/**
 * State for the Egison stream parser.
 */
interface EgisonState {
  tokenize: (stream: StringStream, state: EgisonState) => string | null;
  commentDepth: number;
}

function makeKeywords(str: string): Record<string, boolean> {
  const obj: Record<string, boolean> = {};
  const words = str.split(' ');
  for (const w of words) {
    obj[w] = true;
  }
  return obj;
}

const typeKeywords = makeKeywords(
  'class instance inductive extends declare'
);

const defKeywords = makeKeywords('def let in where');

const controlKeywords = makeKeywords(
  'if then else match matchDFS matchAll matchAllDFS as with do seq loop forall'
);

const otherKeywords = makeKeywords(
  'matcher algebraicDataMatcher memoizedLambda cambda capply function ' +
    'withSymbols pattern expression ' +
    'infixr infixl infix ' +
    'load loadFile execute'
);

const tensorKeywords = makeKeywords(
  'tensor generateTensor contract tensorMap tensorMap2 ' +
    'transpose flipIndices subrefs suprefs userRefs'
);

const builtinTypes = makeKeywords(
  'Integer MathExpr Float Bool Char String IO ' +
    'Matcher Pattern Tensor Vector Matrix DiffForm List'
);

const constants = makeKeywords('True False undefined something');

const testKeywords = makeKeywords('assert assertEqual');

function isIdentChar(ch: string): boolean {
  return /[\w']/.test(ch);
}

function isOpChar(ch: string): boolean {
  return /[+\-*\/=<>!&|^%.:~?∂∇∫∑∏√±×÷≠≤≥∞∈∉∀∃∧∨¬⊕⊗⊥⊤⊆⊇⊂⊃∪∩]/.test(ch);
}

function isGreek(ch: string): boolean {
  return /[αβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]/.test(ch);
}

function tokenBlockComment(
  stream: StringStream,
  state: EgisonState
): string | null {
  let prev: string | null = null;
  while (!stream.eol()) {
    const ch = stream.next()!;
    if (prev === '{' && ch === '-') {
      state.commentDepth++;
    } else if (prev === '-' && ch === '}') {
      state.commentDepth--;
      if (state.commentDepth <= 0) {
        state.commentDepth = 0;
        state.tokenize = tokenBase;
        return 'comment';
      }
    }
    prev = ch;
  }
  return 'comment';
}

function tokenString(
  stream: StringStream,
  state: EgisonState
): string | null {
  let escaped = false;
  while (!stream.eol()) {
    const ch = stream.next()!;
    if (ch === '"' && !escaped) {
      state.tokenize = tokenBase;
      return 'string';
    }
    escaped = !escaped && ch === '\\';
  }
  return 'string';
}

function tokenBase(
  stream: StringStream,
  state: EgisonState
): string | null {
  const ch = stream.next()!;

  // Line comment: --
  if (ch === '-' && stream.eat('-')) {
    stream.skipToEnd();
    return 'comment';
  }

  // Block comment: {- ... -}
  if (ch === '{' && stream.eat('-')) {
    state.commentDepth++;
    state.tokenize = tokenBlockComment;
    return tokenBlockComment(stream, state);
  }

  // String literal
  if (ch === '"') {
    state.tokenize = tokenString;
    return tokenString(stream, state);
  }

  // Character literal
  if (ch === "'") {
    if (stream.eat('\\')) {
      stream.next();
    } else {
      stream.next();
    }
    stream.eat("'");
    return 'string';
  }

  // Pattern variable: $x
  if (ch === '$') {
    stream.match(/[a-zA-Z_][a-zA-Z0-9_']*/, true);
    return 'variableName.special';
  }

  // Value pattern: #x, #(expr)
  if (ch === '#') {
    stream.match(/[a-zA-Z_][a-zA-Z0-9_']*/, true);
    return 'atom';
  }

  // Numbers
  if (/\d/.test(ch)) {
    stream.match(/\d*/, true);
    if (stream.eat('.')) {
      stream.match(/\d+/, true);
    }
    if (stream.eat(/[eE]/)) {
      stream.eat(/[+-]/);
      stream.match(/\d+/, true);
    }
    return 'number';
  }

  // Negative number
  if (ch === '-' && /\d/.test(stream.peek() || '')) {
    stream.match(/\d*/, true);
    if (stream.eat('.')) {
      stream.match(/\d+/, true);
    }
    return 'number';
  }

  // Brackets
  if (/[()[\]{}]/.test(ch)) {
    return 'bracket';
  }

  // Tensor bracket: [| ... |]
  if (ch === '[' && stream.eat('|')) {
    return 'bracket';
  }
  if (ch === '|' && stream.eat(']')) {
    return 'bracket';
  }

  // Assignment operator :=
  if (ch === ':' && stream.eat('=')) {
    return 'operator';
  }

  // Cons operator ::
  if (ch === ':' && stream.eat(':')) {
    return 'operator';
  }

  // Arrow operators
  if (ch === '-' && stream.eat('>')) {
    return 'operator';
  }
  if (ch === '=' && stream.eat('>')) {
    return 'operator';
  }

  // Backslash (lambda)
  if (ch === '\\') {
    return 'keyword';
  }

  // Operators
  if (isOpChar(ch)) {
    stream.eatWhile(isOpChar);
    return 'operator';
  }

  // Greek letters
  if (isGreek(ch)) {
    stream.eatWhile(isGreek);
    return 'variableName.definition';
  }

  // Identifiers and keywords
  if (/[a-zA-Z_]/.test(ch)) {
    stream.eatWhile(isIdentChar);
    const word = stream.current();

    if (typeKeywords.propertyIsEnumerable(word)) return 'keyword';
    if (defKeywords.propertyIsEnumerable(word)) return 'keyword';
    if (controlKeywords.propertyIsEnumerable(word)) return 'keyword';
    if (otherKeywords.propertyIsEnumerable(word)) return 'keyword';
    if (tensorKeywords.propertyIsEnumerable(word)) return 'keyword';
    if (builtinTypes.propertyIsEnumerable(word)) return 'typeName';
    if (constants.propertyIsEnumerable(word)) return 'atom';
    if (testKeywords.propertyIsEnumerable(word)) return 'keyword';

    // User-defined types (uppercase start)
    if (/^[A-Z]/.test(word)) return 'typeName';

    return 'variableName';
  }

  return null;
}

/**
 * CodeMirror 6 stream parser for Egison.
 */
const egisonStreamParser: StreamParser<EgisonState> = {
  startState: (): EgisonState => ({
    tokenize: tokenBase,
    commentDepth: 0
  }),

  token: (stream: StringStream, state: EgisonState): string | null => {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  },

  languageData: {
    commentTokens: {
      line: '--',
      block: { open: '{-', close: '-}' }
    }
  }
};

const egisonLanguage = StreamLanguage.define(egisonStreamParser);

/**
 * JupyterLab plugin that registers the Egison language for CodeMirror.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-egison:plugin',
  description: 'Egison syntax highlighting for JupyterLab',
  autoStart: true,
  requires: [IEditorLanguageRegistry],
  activate: (
    _app: JupyterFrontEnd,
    registry: IEditorLanguageRegistry
  ): void => {
    registry.addLanguage({
      name: 'egison',
      mime: 'text/x-egison',
      displayName: 'Egison',
      extensions: ['egi'],
      support: new LanguageSupport(egisonLanguage)
    });
    console.log('jupyterlab-egison: Egison language registered');
  }
};

export default plugin;
