<template>
  <header>
    <div class="m-4">
      <h1>근처 은행 검색</h1>
      <div class="m-4">
        <select v-model="result" id="keyword" class="custom-border">
          <option value="" selected disabled>은행 선택</option>
          <option v-for="(bank, index) in banks" :key="index" :value="bank">
            {{ bank }}
          </option>
        </select>
        |
        <input type="text" id="region" size="20" placeholder="내 근처 지역 입력" class="custom-border" />
        <button @click="searchPlaces" class="custom-border">&nbsp;&nbsp;찾기&nbsp;&nbsp;</button>
      </div>
    </div>
  </header>
  <!-- 카카오맵 출력 부분 -->
  <main>

      <div id="menu_wrap" class="bg_white">
        <div class="option">
        </div>
      </div>

    <div class="flex">
      <div id="map" class="map child"></div>
      <div> 
        <ul id="placesList"></ul>
        <div id="pagination"></div>
      </div>
    </div>
  </main>
</template>

<script>
const KAKAO_MAP_KEY = import.meta.env.VITE_KAKAO_MAP_KEY

export default {
  data() {
    return {
      selectBank: '',
      banks: ['국민은행', '신한은행', '우리은행', '하나은행', '농협은행', 'IBK기업은행', '산업은행', '새마을금고', '신협', '수협', '광주은행', '전북은행', '대구은행', '경남은행', '부산은행', '제주은행', 'SC제일은행']
    }
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initMap()
    } else {
      this.addKakaoMapScript()
    }
  },
  methods: {
    addKakaoMapScript() {
      const script = document.createElement("script")
      script.onload = () => kakao.maps.load(this.initMap)
      script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_MAP_KEY}&libraries=services`
      document.head.appendChild(script);
    },
    initMap() {
      navigator.geolocation.getCurrentPosition(position => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const mapContainer = document.getElementById("map")
        const mapOption = {
          center: new kakao.maps.LatLng(latitude, longitude),
          level: 3,
        };

        this.map = new kakao.maps.Map(mapContainer, mapOption)
        this.ps = new kakao.maps.services.Places()
        this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
        this.markers = []
      })
    },
    searchPlaces() {
      const keyword = document.getElementById("keyword").value.trim();
      const region = document.getElementById("region").value.trim(); // 지역 입력 값 가져오기

      if (!keyword || !region) {
        alert("은행명과 지역을 모두 입력해주세요!");
        return;
      }

      const query = keyword + ' ' + region; // 지역 정보를 은행와 합침

      this.ps.keywordSearch(query, this.placesSearchCB.bind(this)); // 합친 쿼리로 검색 수행
    },
    placesSearchCB(data, status, pagination) {
      if (status === kakao.maps.services.Status.OK) {
        this.displayPlaces(data);
        this.displayPagination(pagination);
      } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        alert("검색 결과가 존재하지 않습니다.");
      } else if (status === kakao.maps.services.Status.ERROR) {
        alert("검색 결과 중 오류가 발생했습니다.");
      }
    },
    displayPlaces(places) {
      const listEl = document.getElementById("placesList");
      const bounds = new kakao.maps.LatLngBounds();

      this.removeAllChildNodes(listEl);
      this.removeMarker();

      const maxItemsPerPage = 5;
      const startIndex = (pagination.current - 1) * maxItemsPerPage;
      const endIndex = Math.min(startIndex + maxItemsPerPage, places.length);
      

      places.reverse().forEach((place, i) => {
        const placePosition = new kakao.maps.LatLng(place.y, place.x);
        const marker = this.addMarker(placePosition, i);
        const itemEl = this.getListItem(i, place);

        bounds.extend(placePosition);

        kakao.maps.event.addListener(marker, "mouseover", () => {
          this.displayInfowindow(marker, place.place_name);
        });

        kakao.maps.event.addListener(marker, "mouseout", () => {
          this.infowindow.close();
        });

        itemEl.onmouseover = () => {
          this.displayInfowindow(marker, place.place_name);
        };

        itemEl.onmouseout = () => {
          this.infowindow.close();
        };

        listEl.appendChild(itemEl);
      });

      this.map.setBounds(bounds);
    },
    getListItem(index, place) {
      const el = document.createElement("li");
      const itemStr = `
        <span class="markerbg marker_${index + 1}"></span>
        <div class="info">
          <h5>${place.place_name}</h5>
          ${place.road_address_name ? `<span>${place.road_address_name}</span><span class="jibun gray">${place.address_name}</span>` : `<span>${place.address_name}</span>`}
          <span class="tel">${place.phone}</span>
        </div>
      `;
      el.innerHTML = itemStr;
      el.className = "item";
      return el;
    },
    addMarker(position, idx) {
      // 핀 이미지
      const imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png";
      const imageSize = new kakao.maps.Size(36, 37);
      const imgOptions = {
        spriteSize: new kakao.maps.Size(36, 691),
        spriteOrigin: new kakao.maps.Point(0, idx * 46 + 10),
        offset: new kakao.maps.Point(13, 37),
      };
      const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
      const marker = new kakao.maps.Marker({
        position: position,
        image: markerImage,
      });

      marker.setMap(this.map);
      this.markers.push(marker);

      return marker;
    },
    removeMarker() {
      this.markers.forEach((marker) => marker.setMap(null));
      this.markers = [];
    },
    displayPagination(pagination) {
      const paginationEl = document.getElementById("pagination");

      this.removeAllChildNodes(paginationEl);

      for (let i = 1; i <= pagination.last; i++) {
        const el = document.createElement("a");
        el.href = "#";
        el.innerHTML = i;
        el.className = pagination.current === i ? "on" : "";
        el.onclick = () => {
          pagination.gotoPage(i);
        };
        paginationEl.appendChild(el);
      }
    },
    displayInfowindow(marker, title) {
      const content = `<div style="padding:5px;z-index:1;">${title}</div>`;
      this.infowindow.setContent(content);
      this.infowindow.open(this.map, marker);
    },
    removeAllChildNodes(el) {
      while (el.hasChildNodes()) {
        el.removeChild(el.lastChild);
      }
    },
  },
};
</script>

<style>
body {
  font-family: 'Arial', sans-serif;
}

header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-color: #f8f8f8;
  border-bottom: 1px solid #e2e2e2;
}

header h1 {
  margin: 0;
  font-size: 24px;
}

header .m-4 {
  display: flex;
  align-items: center;
  gap: 10px;
}

.custom-border {
  border: 1px solid #e2e2e2;
  padding: 5px;
  border-radius: 3px;
}

.container {
  margin-top: 20px;
  padding: 10px;
}

.map {
  width: 500px;
  height: 600px;
  border: 1px solid #e2e2e2;
  margin-right: 20px;
}

#placesList {
  list-style: none;
  padding: 0;
  max-height: 600px;
  overflow-y: auto;
}

.item {
  padding: 10px;
  border-bottom: 1px solid #e2e2e2;
  cursor: pointer;
}

.item:hover {
  background-color: #f1f1f1;
}

.info {
  display: flex;
  flex-direction: column;
}

.info h5 {
  margin: 0;
  font-size: 18px;
}

.info span {
  font-size: 14px;
  color: #555;
}

.jibun {
  margin-left: 5px;
  color: #999;
}

#pagination {
  margin-top: 10px;
  text-align: center;
}

#pagination a {
  display: inline-block;
  margin: 0 2px;
  padding: 5px 10px;
  border: 1px solid #ddd;
  color: #333;
  text-decoration: none;
  cursor: pointer;
  border-radius: 3px;
}

#pagination a.on {
  border-color: #0066ff;
  color: #0066ff;
  font-weight: bold;
}

.flex {
  display: flex;
  justify-content: center;
  margin: 0 auto;
}
</style>
