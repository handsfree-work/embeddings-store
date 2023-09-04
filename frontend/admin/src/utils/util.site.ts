import { env } from "./util.env";
export const site = {
  /**
   * @description 更新标题
   * @param {String} title 标题
   */
  title: function (titleText: string) {
    const processTitle = env.TITLE || "宝德AI客服系统";
    window.document.title = `${processTitle}${titleText ? ` | ${titleText}` : ""}`;
  }
};
