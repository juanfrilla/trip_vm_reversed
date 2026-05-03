function watch(obj, name) {
  return new Proxy(obj, {
    get(target, p, receiver) {
      if (
        p === "Math" ||
        p === "isNaN" ||
        p === "encodeURI" ||
        p === "Uint8Array" ||
        p.toString().indexOf("Symbol(Symbol.") != -1
      ) {
        let val = Reflect.get(...arguments);

        return val;
      } else {
        let val = Reflect.get(...arguments);

        console.log(`取值:`, name, `.`, p, `=>`, val);

        return val;
      }
    },

    set(target, p, value, receiver) {
      let val = Reflect.get(...arguments);

      console.log(`设置值:`, name, `.`, p, val, `=>`, value);

      return Reflect.set(...arguments);
    },
  });
}
module.exports = { watch };
