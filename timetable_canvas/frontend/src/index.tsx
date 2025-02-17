import { Streamlit, RenderData } from "streamlit-component-lib";

// Função Timetables
class Timetables {
  el: HTMLElement;
  Timetables: any[];
  week: string[];
  merge: boolean;
  TimetableType: any[];
  leftHandText: any[];
  highlightWeek: string;
  gridOnClick?: (e: { name: string; week: string; index: number; length: number }) => void;
  leftHandWidth: number;
  Gheight: number;
  defaultPalette: string[];
  palette: string[] | boolean;

  constructor(option: any) {
    this.el = document.querySelector(option.el)!;
    this.Timetables = option.timetables || [];
    this.week = option.week || [];
    this.merge = typeof option.merge === "boolean" ? option.merge : true;
    this.TimetableType = option.timetableType || [];
    this.leftHandText = [];
    this.highlightWeek = option.highlightWeek || "";
    this.gridOnClick = typeof option.gridOnClick === "function" ? option.gridOnClick : undefined;
    const styles = option.styles || {};
    this.leftHandWidth = styles.leftHandWidth || 40;
    this.Gheight = styles.Gheight || 48;
    this.defaultPalette = ["#71bdb6"];
    this.palette = (typeof styles.palette === "boolean" && !styles.palette)
      ? false
      : (styles.palette || []).concat(this.defaultPalette);
    this._init();
  }

  _init(option?: any) {
    option = option || {};
    const self = this; // Para usar dentro dos closures
    const style = option.styles || {};
    const gridOnClick = option.gridOnClick || this.gridOnClick;
    const merge = typeof option.merge === "boolean" ? option.merge : this.merge;
    const highlightWeek = option.highlightWeek || this.highlightWeek;
    let leftHandText = this.leftHandText;
    const leftHandWidth = style.leftHandWidth || this.leftHandWidth;
    const Gheight = style.Gheight || this.Gheight;
    let palette: string | boolean | any[];
    if (typeof style.palette === "boolean" && !style.palette) {
      palette = false;
    } else {
      palette = style.palette ? (style.palette || []).concat(this.defaultPalette) : this.palette;
    }
    // Note que usamos this.Timetables diretamente para garantir a atualização
    const week = option.week || this.week;
    let TimetableType = JSON.parse(JSON.stringify(option.timetableType || this.TimetableType));
    const deepCopyTimetableType = option.timetableType || this.TimetableType;
    const TimetableTypeLength = TimetableType.length;
    this.Timetables.forEach(function (item: string[], index: any) {
      if (item.length < TimetableTypeLength) {
        for (let i = 0; i < TimetableTypeLength - item.length; i++) {
          item.push("");
        }
      }
    });
    if (option.setNewOption) {
      this.el.removeChild(this.el.childNodes[0]);
    }
    const courseWrapper = document.createElement("div");
    courseWrapper.id = "courseWrapper";
    courseWrapper.className = "container";
    courseWrapper.style.position = "relative";
    courseWrapper.style.paddingLeft = leftHandWidth + "px";
    courseWrapper.style.border = "1px solid #dbdbdb";
    TimetableType.forEach(function (item: any[], index: number) {
      item.unshift(index + 1);
    });
    const leftHand = document.createElement("div");
    leftHand.className = "Courses-leftHand";
    leftHand.style.position = "absolute";
    leftHand.style.left = "0";
    leftHand.style.top = "0";
    leftHand.style.width = leftHandWidth + "px";

    const timetable = this.Timetables[0].map(function (v: any, i: any) {
      return [];
    });
    timetable.forEach(function (item: any, index: string | number) {
      self.Timetables.forEach(function (val: { [x: string]: any }, i: any) {
        timetable[index].push(val[index]);
      });
    });
    const listMerge: { [key: number]: any[] } = [];
    if (merge) {
      self.Timetables.forEach(function (list: any[], i: string | number) {
        if (!listMerge[i as number]) {
          listMerge[i as number] = [];
        }
        list.forEach(function (item: any, index: number) {
          if (!index) {
            return listMerge[i as number].push({ name: item, length: 1 });
          }
          if (item === (listMerge[i as number][index - 1] || {}).name && item) {
            const sameIndex = (listMerge[i as number][index - 1] || {}).sameIndex;
            if (sameIndex || sameIndex === 0) {
              listMerge[i as number][sameIndex].length++;
              return listMerge[i as number].push({ name: item, length: 0, sameIndex: sameIndex });
            }
            listMerge[i as number][index - 1].length++;
            return listMerge[i as number].push({ name: item, length: 0, sameIndex: index - 1 });
          } else {
            return listMerge[i as number].push({ name: item, length: 1 });
          }
        });
      });
    }
    const head = document.createElement("div");
    head.style.overflow = "hidden";
    head.className = "Courses-head row";
    week.forEach(function (item: string, index: number) {
      const weekItem = document.createElement("div");
      const highlightClass = highlightWeek === (index + 1).toString() ? "highlight-week " : "";
      weekItem.className = highlightClass + "Courses-head-" + (index + 1) + " col";
      weekItem.innerText = item;
      head.appendChild(weekItem);
    });
    courseWrapper.appendChild(head);
    const courseListContent = document.createElement("div");
    courseListContent.className = "Courses-content";
    let paletteIndex = 0;
    timetable.forEach((values: any[], index: number) => {
      const courseItems = document.createElement("ul");
      courseItems.className = "stage_" + ((TimetableType[0] || [])[0] || "none");
      courseItems.style.listStyle = "none";
      courseItems.style.padding = "0px";
      courseItems.style.margin = "0px";
      courseItems.style.minHeight = Gheight + "px";
      --(TimetableType[0] || [])[2];
      if (!((TimetableType[0] || [])[2])) {
        TimetableType.shift();
      }
      values.forEach((item: string, i: number) => {
        if (i > week.length - 1) {
          return;
        }
        const courseItem = document.createElement("li");
        courseItem.style.float = "left";
        courseItem.style.fontSize = "12px";
        courseItem.style.width = "20%";
        courseItem.style.height = Gheight + "px";
        courseItem.style.boxSizing = "border-box";
        courseItem.style.position = "relative";

        // Se for célula mesclada
        if (merge && listMerge[i][index].length > 1) {
          const mergeDom = document.createElement("span");
          mergeDom.style.position = "absolute";
          mergeDom.style.zIndex = "9";
          mergeDom.style.width = "100%";
          mergeDom.style.height = Gheight * listMerge[i][index].length + "px";
          mergeDom.style.left = "0";
          mergeDom.style.top = "0";
          if (Array.isArray(palette)) {
            mergeDom.style.backgroundColor = palette[paletteIndex];
            mergeDom.style.color = "#fff";
            paletteIndex++;
            if (paletteIndex >= palette.length) {
              paletteIndex = 0;
            }
          }
          mergeDom.innerText = listMerge[i][index].name;
          mergeDom.className = "course-hasContent";
          courseItem.appendChild(mergeDom);
        } else {
          if (merge && listMerge[i][index].length === 0) {
            courseItem.innerText = "";
          } else {
            if (item && palette) {
              courseItem.style.backgroundColor = (palette as string[])[paletteIndex];
              courseItem.style.color = "#fff";
              paletteIndex = 0;
            } else if (item) {
              courseItem.className = "course-hasContent";
            }
            courseItem.innerText = item || "";
          }
        }

        // Define índices para o callback
        const rowIndex = index;
        const colIndex = i;
        courseItem.onclick = (e: MouseEvent) => {
          // Usa o target clicado
          const target = e.currentTarget as HTMLLIElement;
          // Remove a classe ativa de todas as células
          document.querySelectorAll(".Courses-content ul li").forEach((v: Element) => {
            (v as HTMLElement).classList.remove("grid-active");
          });
          target.classList.add("grid-active");

          // Verifica se a célula possui um <span> (caso seja mesclada)
          let currentValue = "";
          const spanChild = target.querySelector("span") as HTMLElement | null;
          if (spanChild) {
            currentValue = spanChild.innerText;
          } else {
            currentValue = target.innerText;
          }
          // Exibe um prompt para editar/adicionar o valor
          const newValue = prompt("Digite o novo valor para este horário:", currentValue);
          if (newValue === null) return; // usuário cancelou

          // Atualiza o valor exibido na célula
          if (spanChild) {
            spanChild.innerText = newValue;
          } else {
            target.innerText = newValue;
          }

          // Atualiza o estilo da célula conforme o conteúdo
          if (newValue.trim() !== "") {
            // Atualiza o fundo e a cor do texto para indicar que há conteúdo
            target.style.backgroundColor = (Array.isArray(palette) && palette.length > 0 ? palette[0] : "#71bdb6");
            target.style.color = "#fff";
            target.classList.add("course-hasContent");
          } else {
            target.style.backgroundColor = "";
            target.style.color = "";
            target.classList.remove("course-hasContent");
          }

          // Atualiza o array original (propriedade da instância)
          self.Timetables[rowIndex][colIndex] = newValue;
          const info = {
            name: newValue,
            week: week[colIndex],
            index: rowIndex + 1,
            length: merge ? listMerge[colIndex][rowIndex].length : 1
          };
          gridOnClick && gridOnClick(info);
          Streamlit.setComponentValue(self.Timetables);
        };

        courseItems.appendChild(courseItem);
      });
      courseListContent.appendChild(courseItems);
    });
    courseWrapper.appendChild(courseListContent);
    courseWrapper.appendChild(leftHand);
    this.el.appendChild(courseWrapper);
    const courseItemDom = document.querySelector(".stage_1 li") || document.querySelector(".stage_none li");
    const courseItemDomHeight = courseItemDom ? (courseItemDom as HTMLElement).offsetHeight : 0;
    const coursesHeadDom = document.querySelector(".Courses-head") as HTMLElement;
    const coursesHeadDomHeight = coursesHeadDom ? coursesHeadDom.offsetHeight : 0;
    const leftHandTextDom = document.createElement("div");
    leftHandTextDom.className = "left-hand-TextDom";
    leftHandTextDom.style.height = coursesHeadDomHeight + "px";
    leftHandTextDom.style.boxSizing = "border-box";
    leftHandTextDom.style.marginTop = "10px";

    leftHandText = deepCopyTimetableType.map(function (item: any) {
      return item[0].name;
    });

    leftHandText.forEach(function (item) {
      const leftHandTextItem = document.createElement("div");
      leftHandTextItem.className = "left-hand-Text";
      leftHandTextItem.innerText = item.toString();
      const height = courseItemDomHeight * (merge ? (deepCopyTimetableType.shift() || [])[1] : 1) + "px";
      leftHandTextItem.style.height = height;
      leftHandTextDom.appendChild(leftHandTextItem);
    });
    leftHand.appendChild(leftHandTextDom);
  }
}

// Função de renderização do componente
function onRender(event: Event): void {
  const data = (event as CustomEvent<RenderData>).detail;
  const timetables = data.args.timetables;
  const week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
  const timetableType = data.args.timetableType;
  const key = data.args.key;
  const Gheight = data.args.Gheight;
  const highlightWeek = new Date().getDay();
  const styles = {
    Gheight: Gheight,
    leftHandWidth: 60,
    palette: [
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6",
      "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6", "#71bdb6"
    ]
  };

  // Botão para capturar e baixar a imagem (se necessário)
  const captureButton = document.querySelector(".capture");
  if (captureButton) {
    captureButton.setAttribute("onclick", `captureAndDownloadPNG('${key}')`);
  }

  // Cria um ID único para o container do timetable
  const containerId = `coursesTable-${key}`;

  // Verifica se o container já existe; caso contrário, cria-o
  let container = document.getElementById(containerId);
  if (!container) {
    container = document.createElement("div");
    container.id = containerId;
    document.body.appendChild(container);
  } else {
    container.innerHTML = "";
  }

  // Inicializa o timetable
  new Timetables({
    el: `#${containerId}`,
    timetables: timetables,
    week: week,
    timetableType: timetableType,
    highlightWeek: highlightWeek.toString(),
    styles: styles
  });

  Streamlit.setFrameHeight();
}

document.addEventListener("DOMContentLoaded", () => {
  Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
  Streamlit.setComponentReady();
  Streamlit.setFrameHeight();
});

function captureAndDownloadPNG(key: any): any {
  throw new Error("Function not implemented.");
}