// import asyncComponent from './asyncComponent';
import asyncRoute from './asyncComponent';


export { default as App } from '../app'
export const CollegeList = asyncRoute(() => System.import('../apps/college/CollegeList'));
export const CollegeDetail = asyncRoute(() => System.import('../apps/college/CollegeDetail'));
export const CourseList = asyncRoute(() => System.import('../apps/course/CourseList'));
export const CourseDetail = asyncRoute(() => System.import('../apps/course/CourseDetail'));
export const UniversityList = asyncRoute(() => System.import('../apps/university/UniversityList'));
export const UniversityDetail = asyncRoute(() => System.import('../apps/university/UniversityDetail'));
export const AdmissionList = asyncRoute(() => System.import('../apps/admission/AdmissionList'));
export const AdmissionDetail = asyncRoute(() => System.import('../apps/admission/AdmissionDetail'));
export const CareerList = asyncRoute(() => System.import('../apps/career/CareerList'));
export const CareerDetail = asyncRoute(() => System.import('../apps/career/CareerDetail'));
export const EventList = asyncRoute(() => System.import('../apps/event/EventList'));
export const EventDetail = asyncRoute(() => System.import('../apps/event/EventDetail'));
export const NewsList = asyncRoute(() => System.import('../apps/news/NewsList'));
export const NewsDetail = asyncRoute(() => System.import('../apps/news/NewsDetail'));
export const ScholarshipList = asyncRoute(() => System.import('../apps/scholarship/ScholarshipList'));
export const ScholarshipDetail = asyncRoute(() => System.import('../apps/scholarship/ScholarshipDetail'));
export const VacancyList = asyncRoute(() => System.import('../apps/vacancy/VacancyList'));
export const VacancyDetail = asyncRoute(() => System.import('../apps/vacancy/VacancyDetail'));
export const CategoryList = asyncRoute(() => System.import('../apps/categories/CategoryList'));
export const RankList = asyncRoute(() => System.import('../apps/rank/RankList'));
export const RankDetail = asyncRoute(() => System.import('../apps/rank/RankDetail'));
export const FacultyCourseList = asyncRoute(() => System.import('../apps/faculty/FacultyCourseList'));
export const LoginForm = asyncRoute(() => System.import('../apps/users/components/LoginForm'));
export const Profile = asyncRoute(() => System.import('../apps/users/components/Profile'));
export const ChangePassword = asyncRoute(() => System.import('../apps/users/components/ChangePassword'));
export const ResetPassword = asyncRoute(() => System.import('../apps/users/components/ResetPassword'));
export const ResetPasswordForm = asyncRoute(() => System.import('../apps/users/components/ResetPasswordForm'));
export const SignUpForm = asyncRoute(() => System.import('../apps/users/components/SignUpForm'));
export const Credit = asyncRoute(() => System.import('./Credit'));
export { default as Header } from './Header';
export { default as Footer } from './Footer'
export { default as LoadingComponent } from './LoadingComponent'
export const ShortList = asyncRoute(() => System.import('./ShortList'));
export const PageDetail = asyncRoute(() => System.import('../apps/page/PageDetail'));
export const SearchList = asyncRoute(() => System.import('../apps/search/SearchList'));
export const CouncilList = asyncRoute(() => System.import('../apps/council/CouncilList'));
export const CouncilDetail = asyncRoute(() => System.import('../apps/council/CouncilDetail'));

// export const App = asyncComponent(() => import('../app')
//   .then(module => module.default));
// export const CollegeList = asyncComponent(() => import('../apps/college/CollegeList')
//   .then(module => module.default));
// export const CollegeDetail = asyncComponent(() => import('../apps/college/CollegeDetail')
//   .then(module => module.default));
// export const CourseList = asyncComponent(() => import('../apps/course/CourseList')
//   .then(module => module.default));
// export const CourseDetail = asyncComponent(() => import('../apps/course/CourseDetail')
//   .then(module => module.default));
// export const UniversityList = asyncComponent(() => import('../apps/university/UniversityList')
//   .then(module => module.default));
// export const UniversityDetail = asyncComponent(() => import('../apps/university/UniversityDetail')
//   .then(module => module.default));
// export const AdmissionList = asyncComponent(() => import('../apps/admission/AdmissionList')
//   .then(module => module.default));
// export const AdmissionDetail = asyncComponent(() => import('../apps/admission/AdmissionDetail')
//   .then(module => module.default));
// export const CareerList = asyncComponent(() => import('../apps/career/CareerList')
//   .then(module => module.default));
// export const CareerDetail = asyncComponent(() => import('../apps/career/CareerDetail')
//   .then(module => module.default));
// export const EventList = asyncComponent(() => import('../apps/event/EventList')
//   .then(module => module.default));
// export const EventDetail = asyncComponent(() => import('../apps/event/EventDetail')
//   .then(module => module.default));
// export const NewsList = asyncComponent(() => import('../apps/news/NewsList')
//   .then(module => module.default));
// export const NewsDetail = asyncComponent(() => import('../apps/news/NewsDetail')
//   .then(module => module.default));
// export const ScholarshipList = asyncComponent(() => import('../apps/scholarship/ScholarshipList')
//   .then(module => module.default));
// export const ScholarshipDetail = asyncComponent(() => import('../apps/scholarship/ScholarshipDetail')
//   .then(module => module.default));
// export const VacancyList = asyncComponent(() => import('../apps/vacancy/VacancyList')
//   .then(module => module.default));
// export const VacancyDetail = asyncComponent(() => import('../apps/vacancy/VacancyDetail')
//   .then(module => module.default));
// export const CategoryList = asyncComponent(() => import('../apps/categories/CategoryList')
//   .then(module => module.default));
// export const RankList = asyncComponent(() => import('../apps/rank/RankList')
//   .then(module => module.default));
// export const RankDetail = asyncComponent(() => import('../apps/rank/RankDetail')
//   .then(module => module.default));
// export const FacultyCourseList = asyncComponent(() => import('../apps/faculty/FacultyCourseList')
//   .then(module => module.default));
// export const LoginForm = asyncComponent(() => import('../apps/users/components/LoginForm')
//   .then(module => module.default));
// export const SignUpForm = asyncComponent(() => import('../apps/users/components/SignUpForm')
//   .then(module => module.default));
// export const Header = asyncComponent(() => import('../components/Header')
//   .then(module => module.default));
// export const Footer = asyncComponent(() => import('../components/Footer')
//   .then(module => module.default));
// export const LoadingComponent = asyncComponent(() => import('./LoadingComponent')
//   .then(module => module.default));
// export const ShortList = asyncComponent(() => import('./ShortList')
//   .then(module => module.default));
// export const PageDetail = asyncComponent(() => import('../apps/page/PageDetail')
//   .then(module => module.default));
// export const SearchList = asyncComponent(() => import('../apps/search/SearchList')
//   .then(module => module.default));
// export const CouncilList = asyncComponent(() => import('../apps/council/CouncilList')
//   .then(module => module.default));
// export const CouncilDetail = asyncComponent(() => import('../apps/council/CouncilDetail')
//   .then(module => module.default));